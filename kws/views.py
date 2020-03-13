from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import View
from pydub import AudioSegment
from django.views.generic.edit import FormView
from .forms import KeyWordForm
from .forms import SearchKeyWordForm

import os
import glob
import xml.etree.ElementTree as ET
from django.conf import settings
import pdb


class Analysis(View):

    template_name = 'kws/analysis.html'
    call_to_keyword = {}

    def audio_segment(self, path, kwid, wav_file_path, duration, sample_rate):

        for idx, dur in enumerate(duration):
            # pdb.set_trace()
            seg_file_name = dur[0]+'_'+kwid+'_'+str(idx)+'.wav'
            kw_start = float(dur[2]) * sample_rate * 1000

            start = kw_start - 1500
            end = kw_start + 1500
            if start < 0:
                start = 0
            newAudio = AudioSegment.from_wav(wav_file_path)
            newAudio = newAudio[start:end]
            newAudio.export(path+"/"+seg_file_name, format="wav")
            duration[idx].append(settings.USER['kaldi']
                                 ['kws_segment_wav']+seg_file_name)
        return duration

    def listen_call_keyword(self, wavfile, keyword, kwslist, keyword_id, call_id):
        kwid_to_word = {}
        with open(keyword) as f:
            for line in f.readlines():
                tmp = line.split()
                kwid_to_word[tmp[0]] = tmp[1]

        callid_to_wav = {}
        with open(wavfile) as f:
            for line in f.readlines():
                tmp = line.split()
                callid_to_wav[tmp[0]] = tmp[1]

        tree = ET.parse(kwslist)
        root = tree.getroot()
        duration = []
        for elem in root:
            kwid = elem.attrib['kwid']
            if keyword_id != kwid:
                continue
            word = kwid_to_word[elem.attrib['kwid']]
            for subelem in elem:
                call = subelem.attrib['file']
                if call != call_id:
                    continue
                tbeg = subelem.attrib['tbeg']
                dur = subelem.attrib['dur']
                score = subelem.attrib['score']
                decision = subelem.attrib['decision']
                if decision == 'YES':
                    duration.append([call, word, tbeg, dur])
        duration = self.audio_segment(
            'static/'+settings.USER['kaldi']['kws_segment_wav'],
            keyword_id,
            callid_to_wav[call_id],
            duration,
            int(settings.USER['kaldi']['kws_sample_rate']))
        return duration

    def xml_to_dictinary_key_call(self, keyword, kwslist, wav_path):
        kwid_to_word = {}
        with open(keyword) as f:
            for line in f.readlines():
                tmp = line.split()
                kwid_to_word[tmp[0]] = tmp[1]

        tree = ET.parse(kwslist)
        root = tree.getroot()

        for elem in root:
            kwid = elem.attrib['kwid']
            keyword = kwid_to_word[elem.attrib['kwid']]
            for subelem in elem:
                call = subelem.attrib['file']
                tbeg = subelem.attrib['tbeg']
                dur = subelem.attrib['dur']
                score = subelem.attrib['score']
                decision = subelem.attrib['decision']
                if decision == 'NO':
                    continue
                if call not in self.call_to_keyword:
                    self.call_to_keyword[call] = {}
                if kwid not in self.call_to_keyword[call]:
                    self.call_to_keyword[call][kwid] = keyword

        utt_to_wav = {}
        with open(wav_path) as f:
            for line in f.readlines():
                tmp = line.split()
                wav_file = tmp[1].split('static')
                if tmp[0] in self.call_to_keyword:
                    self.call_to_keyword[tmp[0]]['XWAV'] = wav_file[1]

    def get(self, request, **kwargs):
        context = {}
        if 'call_id' in self.kwargs:
            duration = self.listen_call_keyword(
                settings.USER['kaldi']['kws_upload'] +
                "/wav.scp",
                'kws/data/keywords.txt', 'kws/data/kwslist.xml',
                self.kwargs['keyword_id'],
                self.kwargs['call_id'])
            context = {'duration': duration}
        else:
            self.call_to_keyword = {}
            self.xml_to_dictinary_key_call(
                'kws/data/keywords.txt', 'kws/data/kwslist.xml', settings.USER['kaldi']['kws_upload']+'/wav.scp')
            context = {'call_to_keyword': self.call_to_keyword}

        return render(request, self.template_name, context)


class Keyword(FormView):

    form_class = KeyWordForm
    template_name = 'kws/keyword.html'

    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return render(request, 'kws/keyword.html', {'form': form})

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # pdb.set_trace()
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            keyword_list = form.cleaned_data['keywords'].split(',')
            self.make_raw_list(keyword_list)

            kws_upload = settings.USER['kaldi']['kws_upload']
            file_list = []
            for f in files:
                full_path = kws_upload + '/' + f.name
                file_list.append(full_path)
                self.handle_upload_file(
                    f, full_path)

            self.make_spk_utt(kws_upload, file_list)
            self.run_kaldi_script()
            return redirect('analysis')

        return render(request, 'kws/keyword.html', {'form': form})

    def handle_upload_file(self, f, path):
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def make_raw_list(self, keyword_list):
        with open('kws/data/' + settings.USER['kaldi']['kws_raw_list'], 'w') as f:
            for keyword in keyword_list:
                f.write(keyword.upper() + '\n')

    def run_kaldi_script(self):
        os.system("bash kws/keyword.sh "
                  + settings.USER['kaldi']['home']
                  + ' ' + settings.USER['kaldi']['kws_project']
                  + ' ' + settings.USER['kaldi']['kws_test']
                  + ' ' + settings.USER['kaldi']['kws_tree']
                  + ' ' + settings.USER['kaldi']['kws_upload']
                  + ' ' + settings.USER['kaldi']['kws_raw_list'])

    def make_spk_utt(self, path, file_list):
        utt2spk = open(path+"/utt2spk", 'w')
        spk2utt = open(path+"/spk2utt", 'w')

        with open(path+"/wav.scp", 'w') as f:
            idx = 1
            for file_id in file_list:
                str_idx = 'utt'+str(idx).zfill(4)
                f.write(str_idx+' ' + os.path.abspath(file_id)+'\n')
                idx = idx+1
                utt2spk.write(str_idx+' '+str_idx+'\n')
                spk2utt.write(str_idx+' '+str_idx+'\n')


class SearchKeyword(FormView):

    form_class = SearchKeyWordForm
    template_name = 'kws/search_keyword.html'

    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return render(request, 'kws/search_keyword.html', {'form': form})

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # pdb.set_trace()
        if form.is_valid():
            keywords = form.cleaned_data['keywords'].split(',')
            with open('kws/data/' + settings.USER['kaldi']['kws_raw_list'], 'w') as f:
                for keyword in keywords:
                    f.write(keyword.upper() + '\n')

            os.system("bash kws/search_keyword.sh "
                      + settings.USER['kaldi']['home']
                      + ' ' + settings.USER['kaldi']['kws_project']
                            + ' ' + settings.USER['kaldi']['kws_test']
                            + ' ' + settings.USER['kaldi']['kws_tree']
                            + ' ' + settings.USER['kaldi']['kws_upload']
                            + ' ' + settings.USER['kaldi']['kws_raw_list'])
            return redirect('analysis')

        return render(request, 'kws/search_keyword.html', {'form': form})


class KeywordIndex(View):

    def get(self, request):
        return render(request, 'kws/keyword_index.html')


class Index(View):

    def get(self, request):
        return render(request, 'kws/index.html')


# Create your views here.
