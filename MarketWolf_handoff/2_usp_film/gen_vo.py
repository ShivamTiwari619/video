import json, base64, subprocess, urllib.request, os, re
KEY=os.environ['XI']; VID='NvA7c85NkZVpFBAHHQQ3'
L=[('l1',"Every trader knows when to get in. Very few know when to get out."),
('l2',"Most trades don't go wrong at the entry. They go wrong at the exit."),
('l3',"On MarketWolf, every trade has its exit set before you enter. A target to book your profit, and a stop loss to protect your capital."),
('l4',"You also get trade ideas from SEBI-registered analysts, each one with its profit and stop-loss levels already set."),
('l5',"Indices, stocks and commodities, all in one app. Even gold and crude, till eleven fifty-five at night."),
('l6',"A flat nineteen rupees a trade. Zero AMC. Nothing hidden."),
('l7',"Only liquid instruments. SEBI-registered. Support whenever you need it."),
('l8',"MarketWolf. Trade with discipline.")]
def stt(p):
    r=subprocess.run(['curl','-s','-X','POST','https://api.elevenlabs.io/v1/speech-to-text','-H',f'xi-api-key: {KEY}','-F','model_id=scribe_v1','-F','language_code=en','-F',f'file=@{p}'],capture_output=True,text=True)
    return json.loads(r.stdout).get('text','')
out={}
for k,t in L:
    body={"text":t,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.65,"similarity_boost":0.8,"style":0.0,"use_speaker_boost":True,"speed":0.93}}
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VID}/with-timestamps?output_format=mp3_44100_128",data=json.dumps(body).encode(),headers={"xi-api-key":KEY,"Content-Type":"application/json","User-Agent":"curl/8.5"})
    d=json.loads(urllib.request.urlopen(req,timeout=180).read())
    open(f'vo/{k}.mp3','wb').write(base64.b64decode(d['audio_base64']))
    al=d['alignment']; ch=al['characters']; st=al['character_start_times_seconds']; en=al['character_end_times_seconds']
    txt=''.join(ch); words=[(m.group(),st[m.start()],en[m.end()-1]) for m in re.finditer(r'\S+',txt)]
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y','-i',f'vo/{k}.mp3','-af','areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse','-ar','44100','-ac','1',f'vo/{k}.wav'],check=True)
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'vo/{k}.wav'],capture_output=True,text=True).stdout)
    heard=stt(f'vo/{k}.mp3')
    out[k]={'dur':round(dur,3),'heard':heard,'words':[(w,round(a,3),round(b,3)) for w,a,b in words]}
    print(k,'%.2fs'%dur,'|',heard)
json.dump(out,open('vo/vo.json','w'),indent=1)
