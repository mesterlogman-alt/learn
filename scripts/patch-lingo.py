#!/usr/bin/env python3
"""Patch Lingo Memory HTML: fix crashes, data-loss UX, splash, backups, dialogs."""
from pathlib import Path

SRC = Path("/workspace/attachments/index-1_٠٩١٠٤٦.html")
DST = Path("/workspace/public/lingo.html")

html = SRC.read_text(encoding="utf-8")


def once(old: str, new: str, label: str) -> None:
    global html
    n = html.count(old)
    if n != 1:
        raise SystemExit(f"PATCH FAIL {label}: found {n} occurrences")
    html = html.replace(old, new, 1)
    print("ok", label)


# ---------------------------------------------------------------------------
# 1. CSS: stop hiding all role=status; desktop insets; 6-col nav; dialog
# ---------------------------------------------------------------------------
once(
    """[class*="netlify"],
  [id*="netlify"],
  iframe[src*="netlify"],
  .netlify-badge,
  [role="status"],
  footer[class*="netlify"] {
    display: none !important;
    visibility: hidden !important;
  }""",
    """[class*="netlify-"],
  [id*="netlify-"],
  iframe[src*="netlify"],
  .netlify-badge {
    display: none !important;
  }""",
    "css-netlify-role-status",
)

once(
    "</style>\n\n</head>",
    """
/* ===== Stability / personal-use patches ===== */
.mobile-nav{grid-template-columns:repeat(6,1fr)!important}
@media(max-width:720px){
  .mobile-nav button{font-size:9.5px!important;padding:0 2px}
  .mobile-nav button .ico{width:40px!important;height:40px!important;font-size:18px!important}
}
.app-dialog .modal{width:min(440px,100%);padding:18px}
.app-dialog-msg{margin:0;color:#52657d;font-size:13px;line-height:1.75;white-space:pre-wrap}
.app-dialog-input,.app-dialog-select{width:100%;margin-top:8px}
.backup-list{display:grid;gap:8px;margin-top:8px}
.backup-row{display:flex;justify-content:space-between;gap:8px;align-items:center;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:#f8fbff}
.backup-row b{display:block;font-size:12px}
.backup-row span{font-size:11px;color:var(--muted)}
.library-project.unassigned .library-project-icon{background:linear-gradient(135deg,#8a98aa,#6c7b91)!important}
.gemini-model-row{display:grid;gap:8px;margin-top:8px}
.boot-error{position:fixed;inset:auto 16px 16px 16px;z-index:10000;background:#3b1d22;color:#fff;border-radius:14px;padding:12px 14px;display:none}
.boot-error.show{display:block}
</style>
</head>""",
    "css-stability-block",
)

# ---------------------------------------------------------------------------
# 2. Mobile nav: add stats
# ---------------------------------------------------------------------------
once(
    '<div class="mobile-nav"><button data-page="library" class="active"><span class="ico">⌂</span>المكتبة</button><button data-page="translate"><span class="ico">🌐</span>ترجمة</button><button data-page="dictionary"><span class="ico">📖</span>قاموس</button><button data-page="words"><span class="ico">Aa</span>كلماتي</button><button data-page="settings"><span class="ico">⚙</span>الإعدادات</button></div>',
    '<div class="mobile-nav"><button data-page="library" class="active"><span class="ico">⌂</span>المكتبة</button><button data-page="translate"><span class="ico">🌐</span>ترجمة</button><button data-page="dictionary"><span class="ico">📖</span>قاموس</button><button data-page="words"><span class="ico">Aa</span>كلماتي</button><button data-page="stats"><span class="ico">◌</span>إحصاء</button><button data-page="settings"><span class="ico">⚙</span>إعدادات</button></div>',
    "mobile-nav-stats",
)

# ---------------------------------------------------------------------------
# 3. Gemini model selector + test button
# ---------------------------------------------------------------------------
once(
    '<div class="external-small">النموذج الافتراضي: Gemini 3.5 Flash-Lite. نموذج احتياطي داخلي: Gemini 3.6 Flash.</div>',
    '''<div class="gemini-model-row">
          <label for="geminiModel">نموذج الترجمة</label>
          <select id="geminiModel" class="search">
            <option value="gemini-3.5-flash-lite">Gemini 3.5 Flash-Lite — أسرع وأوفر</option>
            <option value="gemini-3.5-flash">Gemini 3.5 Flash</option>
            <option value="gemini-3.6-flash">Gemini 3.6 Flash — أقوى</option>
          </select>
          <button id="geminiTestBtn" class="ghost" type="button">اختبار الاتصال</button>
        </div>
        <div class="external-small">إن فشل النموذج المختار يُستخدم تلقائيًا النموذج الاحتياطي. المفتاح يُحفظ على هذا الجهاز فقط.</div>''',
    "gemini-model-ui",
)

# ---------------------------------------------------------------------------
# 4. Settings: restore backups card
# ---------------------------------------------------------------------------
once(
    '''<div class="card settings-card">
            <div class="settings-card-head"><div><h3>📊 حالة النظام</h3>''',
    '''<div class="card settings-card">
            <div class="settings-card-head"><div><h3>🛟 نسخ الاسترجاع</h3><p>النسخ التي يحفظها التطبيق تلقائيًا داخل IndexedDB. يمكنك الرجوع لنسخة سابقة إذا حدث خطأ.</p></div><span class="settings-card-badge">محلي</span></div>
            <div id="backupList" class="backup-list"><div class="settings-note">اضغط تحديث لعرض النسخ المحفوظة على هذا الجهاز.</div></div>
            <div class="settings-actions"><button class="ghost" id="refreshBackupsBtn" type="button">تحديث القائمة</button></div>
          </div>

          <div class="card settings-card">
            <div class="settings-card-head"><div><h3>📊 حالة النظام</h3>''',
    "backup-settings-card",
)

# ---------------------------------------------------------------------------
# 5. In-app dialog + boot error
# ---------------------------------------------------------------------------
once(
    '<div id="toast" class="toast"></div>',
    '''<div class="modal-backdrop app-dialog" id="appDialog">
  <div class="modal">
    <div class="modal-head"><h3 id="appDialogTitle">تنبيه</h3>
      <button id="appDialogClose" class="modal-close" type="button" aria-label="إغلاق">✕</button>
    </div>
    <div class="modal-body">
      <p id="appDialogMessage" class="app-dialog-msg"></p>
      <input id="appDialogInput" class="search app-dialog-input" hidden>
      <select id="appDialogSelect" class="search app-dialog-select" hidden></select>
      <div class="modal-actions">
        <button id="appDialogCancel" class="ghost" type="button">إلغاء</button>
        <button id="appDialogOk" class="primary" type="button">موافق</button>
      </div>
    </div>
  </div>
</div>
<div id="bootError" class="boot-error" role="alert"></div>
<div id="toast" class="toast"></div>''',
    "app-dialog-html",
)

# ---------------------------------------------------------------------------
# 6. Desktop-safe insets (don't force 64px on laptop)
# ---------------------------------------------------------------------------
once(
    """  function applyInsets(){
    try{
      const root=document.documentElement;
      const vv=window.visualViewport;
      let bottomGap=0,topGap=0;
      if(vv){
        bottomGap=Math.max(0,window.innerHeight - vv.height - vv.offsetTop);
        topGap=Math.max(0,vv.offsetTop);
      }
      const sab=Math.max(bottomGap,MIN_BOTTOM_RESERVE);
      const sat=Math.max(topGap,MIN_TOP_RESERVE);
      root.style.setProperty('--sab-js',sab+'px');
      root.style.setProperty('--sat-js',sat+'px');
    }catch(e){}
  }""",
    """  function applyInsets(){
    try{
      const root=document.documentElement;
      const vv=window.visualViewport;
      let bottomGap=0,topGap=0;
      if(vv){
        bottomGap=Math.max(0,window.innerHeight - vv.height - vv.offsetTop);
        topGap=Math.max(0,vv.offsetTop);
      }
      const compact=window.matchMedia('(max-width:720px)').matches || (window.matchMedia('(pointer:coarse)').matches && window.innerWidth<900);
      const sab=compact?Math.max(bottomGap,MIN_BOTTOM_RESERVE):Math.max(bottomGap,0);
      const sat=compact?Math.max(topGap,MIN_TOP_RESERVE):Math.max(topGap,0);
      root.style.setProperty('--sab-js',sab+'px');
      root.style.setProperty('--sat-js',sat+'px');
    }catch(e){}
  }""",
    "insets-desktop",
)

# ---------------------------------------------------------------------------
# 7. toast null-safe + in-app dialog helpers
# ---------------------------------------------------------------------------
once(
    "function toast(msg){const t=$('toast');t.textContent=msg;t.classList.add('show');clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove('show'),1800)}",
    r"""function toast(msg){const t=$('toast');if(!t)return;t.textContent=String(msg||'');t.classList.add('show');clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove('show'),2200)}
let _dialogResolver=null;
function closeAppDialog(result){
  const m=$('appDialog');if(m)m.classList.remove('show');
  const r=_dialogResolver;_dialogResolver=null;if(typeof r==='function')r(result);
}
function _openAppDialog({title,message,mode,value,options}){
  return new Promise(resolve=>{
    closeAppDialog(null);
    _dialogResolver=resolve;
    const titleEl=$('appDialogTitle'),msgEl=$('appDialogMessage'),input=$('appDialogInput'),sel=$('appDialogSelect');
    if(titleEl)titleEl.textContent=title||'تنبيه';
    if(msgEl)msgEl.textContent=message||'';
    if(input){input.hidden=mode!=='prompt';input.value=value||'';}
    if(sel){
      sel.hidden=mode!=='select';
      sel.innerHTML=(options||[]).map(o=>'<option value="'+esc(o.value)+'"'+(String(o.value)===String(value)?' selected':'')+'>'+esc(o.label)+'</option>').join('');
    }
    $('appDialog')?.classList.add('show');
    setTimeout(()=>{if(mode==='prompt')input?.focus();else if(mode==='select')sel?.focus();else $('appDialogOk')?.focus();},40);
  });
}
function appPrompt(title,message,def=''){return _openAppDialog({title,message,mode:'prompt',value:def}).then(v=>v===undefined||v===false?null:String(v))}
function appConfirm(title,message){return _openAppDialog({title,message,mode:'confirm'}).then(v=>v===true)}
function appSelect(title,message,options,current){return _openAppDialog({title,message,mode:'select',options,value:current})}
function updateTranslationProviderUI(){/* leftover hook from older multi-provider screen — Gemini-only now */}
""",
    "toast-and-dialogs",
)

# ---------------------------------------------------------------------------
# 8. Repair prompt: actual newlines, not the two-char \n
# ---------------------------------------------------------------------------
once("].join('\\\\n');", "].join('\\n');", "gemini-repair-join")

# ---------------------------------------------------------------------------
# 9. create / rename / delete project — async dialogs + unassigned folder
# ---------------------------------------------------------------------------
once(
    "function createProject(){const raw=prompt('اسم المشروع:','مشروعي الجديد');if(raw===null)return;const name=String(raw).trim();if(!name){toast('اكتب اسمًا للمشروع');return}if(state.projects.some(p=>normalizeProjectName(p.name)===normalizeProjectName(name))){toast('يوجد مشروع بهذا الاسم بالفعل');return}const p={id:id(),name:name.slice(0,120),created:Date.now()};state.projects.unshift(p);state._lastAddProject=p.id;libraryProjectFilter='';save();renderAll();toast('تم إنشاء المشروع')}",
    """function createProject(){appPrompt('مشروع جديد','اكتب اسم المشروع:','مشروعي الجديد').then(raw=>{if(raw===null)return;const name=String(raw).trim();if(!name){toast('اكتب اسمًا للمشروع');return}if(state.projects.some(p=>normalizeProjectName(p.name)===normalizeProjectName(name))){toast('يوجد مشروع بهذا الاسم بالفعل');return}const p={id:id(),name:name.slice(0,120),created:Date.now()};state.projects.unshift(p);state._lastAddProject=p.id;libraryProjectFilter='';save();renderAll();toast('تم إنشاء المشروع')})}""",
    "createProject",
)

once(
    "function renameProject(pid){const p=projectById(pid);if(!p)return;const raw=prompt('اسم المشروع الجديد:',p.name);if(raw===null)return;const name=String(raw).trim();if(!name)return;if(state.projects.some(x=>x.id!==pid&&normalizeProjectName(x.name)===normalizeProjectName(name))){toast('يوجد مشروع بهذا الاسم بالفعل');return}p.name=name.slice(0,120);save();renderAll();toast('تم تعديل اسم المشروع')}",
    "function renameProject(pid){const p=projectById(pid);if(!p)return;appPrompt('تعديل اسم المشروع','الاسم الجديد:',p.name).then(raw=>{if(raw===null)return;const name=String(raw).trim();if(!name)return;if(state.projects.some(x=>x.id!==pid&&normalizeProjectName(x.name)===normalizeProjectName(name))){toast('يوجد مشروع بهذا الاسم بالفعل');return}p.name=name.slice(0,120);save();renderAll();toast('تم تعديل اسم المشروع')})}",
    "renameProject",
)

once(
    "function deleteProject(pid){const p=projectById(pid);if(!p)return;if(!confirm('حذف المشروع فقط؟\\nلن يتم حذف الدروس، وستصبح بدون مشروع.\\n\\n'+p.name))return;state.projects=state.projects.filter(x=>x.id!==pid);state.lessons=state.lessons.map(l=>l.projectId===pid?{...l,projectId:''}:l);if(libraryProjectFilter===pid)libraryProjectFilter='';if(state._lastAddProject===pid)state._lastAddProject='';save();renderAll();toast('تم حذف المشروع وبقيت الدروس كما هي')}",
    "function deleteProject(pid){const p=projectById(pid);if(!p)return;appConfirm('حذف المشروع','حذف المشروع فقط؟ لن تُحذف الدروس، وستظهر في مجلد «دروس بدون مشروع».\\n\\n'+p.name).then(ok=>{if(!ok)return;state.projects=state.projects.filter(x=>x.id!==pid);state.lessons=state.lessons.map(l=>l.projectId===pid?{...l,projectId:''}:l);if(libraryProjectFilter===pid)libraryProjectFilter='__unassigned__';if(state._lastAddProject===pid)state._lastAddProject='';save();renderAll();toast('تم حذف المشروع — الدروس في مجلد «دروس بدون مشروع»')})}",
    "deleteProject",
)

# ---------------------------------------------------------------------------
# 10. renderLibrary — show unassigned lessons instead of hiding them
# ---------------------------------------------------------------------------
once(
    """function renderLibrary(){
  const selected=projectById(libraryProjectFilter);
  const heading=$('libraryHeading'),sub=$('librarySubheading'),bar=$('libraryFolderBar'),tools=$('libraryLessonTools'),listHost=$('libraryList'),projects=$('libraryProjects');
  if(selected){
    heading.textContent='المشروع';sub.textContent='الدروس هنا هي ملفات هذا المشروع. يمكنك فتح الدرس أو تعديل اسمه أو حذفه.';
    bar.hidden=false;bar.innerHTML=`<div class="folder-left"><span class="folder-icon">📁</span><span class="folder-name">${esc(selected.name)}</span><span id="libraryLessonCount" class="folder-count"></span></div><button class="library-folder-back" type="button" data-project-filter="">← المشروعات</button>`;
    tools.hidden=false;listHost.hidden=false;
  }else{
    heading.textContent='المشروعات';sub.textContent='اعتبر كل مشروع مجلدًا، وتوجد الدروس داخله مثل الملفات في مدير ملفات الهاتف.';
    bar.hidden=true;bar.innerHTML='';tools.hidden=true;listHost.hidden=true;listHost.innerHTML='';
  }
  if(!selected){renderProjectUI();return;}
  const q=($('lessonSearch')?.value||'').toLowerCase().trim();const f=$('libraryFilter')?.value||'recent';
  let list=state.lessons.filter(l=>l.projectId===selected.id&&(!q||l.title.toLowerCase().includes(q)));
  const lessonCountLabel=$('libraryLessonCount');
  if(f==='known')list.sort((a,b)=>analyzeLessonStats(b).knownPct-analyzeLessonStats(a).knownPct);
  else if(f==='created')list.sort((a,b)=>(b.created||0)-(a.created||0));
  else if(f==='name')list.sort((a,b)=>a.title.localeCompare(b.title,'ar',{numeric:true,sensitivity:'base'}));
  else list.sort((a,b)=>(b.lastOpened||b.created||0)-(a.lastOpened||a.created||0));
  if(lessonCountLabel)lessonCountLabel.textContent=list.length?`${list.length} ${list.length===1?'درس':'دروس'}`:'';
  listHost.innerHTML=list.length?list.map((l,i)=>lessonRow(l,f==='known'?i+1:0)).join(''):('<div class="card library-empty-folders"><div class="empty-folder-icon">📄</div><b>المجلد فارغ</b><p>لا توجد دروس داخل هذا المشروع. أضف درسًا من شاشة «إضافة درس» واختر هذا المشروع.</p></div>');
  renderProjectUI();
}""",
    """function renderLibrary(){
  const isUnassigned=libraryProjectFilter==='__unassigned__';
  const selected=isUnassigned?null:projectById(libraryProjectFilter);
  const heading=$('libraryHeading'),sub=$('librarySubheading'),bar=$('libraryFolderBar'),tools=$('libraryLessonTools'),listHost=$('libraryList'),projects=$('libraryProjects');
  const showLessons=isUnassigned||!!selected;
  if(showLessons){
    heading.textContent=isUnassigned?'دروس بدون مشروع':'المشروع';
    sub.textContent=isUnassigned?'هذه الدروس لا تتبع مشروعًا حاليًا. يمكنك فتحها أو نقلها إلى مشروع.':'الدروس هنا هي ملفات هذا المشروع. يمكنك فتح الدرس أو تعديل اسمه أو حذفه.';
    const folderName=isUnassigned?'دروس بدون مشروع':selected.name;
    bar.hidden=false;bar.innerHTML=`<div class="folder-left"><span class="folder-icon">${isUnassigned?'📂':'📁'}</span><span class="folder-name">${esc(folderName)}</span><span id="libraryLessonCount" class="folder-count"></span></div><button class="library-folder-back" type="button" data-project-filter="">← المشروعات</button>`;
    tools.hidden=false;listHost.hidden=false;
  }else{
    heading.textContent='المشروعات';sub.textContent='كل مشروع مجلد، والدروس داخله كالملفات. الدروس بلا مشروع تظهر في مجلد مستقل حتى لا تختفي.';
    bar.hidden=true;bar.innerHTML='';tools.hidden=true;listHost.hidden=true;listHost.innerHTML='';
  }
  if(!showLessons){renderProjectUI();return;}
  const q=($('lessonSearch')?.value||'').toLowerCase().trim();const f=$('libraryFilter')?.value||'recent';
  let list=state.lessons.filter(l=>(isUnassigned?!l.projectId:l.projectId===selected.id)&&(!q||l.title.toLowerCase().includes(q)));
  const lessonCountLabel=$('libraryLessonCount');
  if(f==='known')list.sort((a,b)=>analyzeLessonStats(b).knownPct-analyzeLessonStats(a).knownPct);
  else if(f==='created')list.sort((a,b)=>(b.created||0)-(a.created||0));
  else if(f==='name')list.sort((a,b)=>a.title.localeCompare(b.title,'ar',{numeric:true,sensitivity:'base'}));
  else list.sort((a,b)=>(b.lastOpened||b.created||0)-(a.lastOpened||a.created||0));
  if(lessonCountLabel)lessonCountLabel.textContent=list.length?`${list.length} ${list.length===1?'درس':'دروس'}`:'';
  listHost.innerHTML=list.length?list.map((l,i)=>lessonRow(l,f==='known'?i+1:0)).join(''):('<div class="card library-empty-folders"><div class="empty-folder-icon">📄</div><b>المجلد فارغ</b><p>'+(isUnassigned?'لا توجد دروس خارج المشروعات.':'لا توجد دروس داخل هذا المشروع. أضف درسًا من شاشة «ترجمة Gemini» واختر هذا المشروع.')+'</p></div>');
  renderProjectUI();
}""",
    "renderLibrary-unassigned",
)

# ---------------------------------------------------------------------------
# 11. renderProjectUI — unassigned card
# ---------------------------------------------------------------------------
once(
    "host.innerHTML=cards || `<div class=\"card library-empty-folders\"><div class=\"empty-folder-icon\">📁</div><b>لا توجد مشروعات بعد</b><p>أنشئ مشروعًا أولًا، ثم أضف الدروس إليه من شاشة «إضافة درس».</p><button class=\"primary\" data-create-project>＋ إنشاء مشروع</button></div>`;",
    """const unassignedCount=state.lessons.filter(l=>!l.projectId).length;
    const unassignedCard=unassignedCount?`<article class="library-project unassigned ${libraryProjectFilter==='__unassigned__'?'active':''}" data-project-filter="__unassigned__" aria-label="فتح دروس بدون مشروع">
        <div class="library-project-top"><span class="library-project-icon">📂</span><span class="library-project-name">دروس بدون مشروع</span></div>
        <div class="library-project-meta"><span class="library-project-count">${unassignedCount} ${unassignedCount===1?'درس':'دروس'}</span><span class="library-project-arrow">فتح المجلد ‹</span></div>
      </article>`:'';
    host.innerHTML=(unassignedCard+cards) || `<div class="card library-empty-folders"><div class="empty-folder-icon">📁</div><b>لا توجد مشروعات بعد</b><p>أنشئ مشروعًا أولًا، ثم أضف درسًا من شاشة «ترجمة Gemini».</p><button class="primary" data-create-project>＋ إنشاء مشروع</button></div>`;""",
    "renderProjectUI-unassigned",
)

# ---------------------------------------------------------------------------
# 12. lesson title / delete / settings confirms
# ---------------------------------------------------------------------------
once(
    "function editLessonTitle(lid){const l=state.lessons.find(x=>x.id===lid);if(!l)return;const next=prompt('اسم الدرس الجديد:',l.title);if(next===null)return;const title=String(next).trim();if(!title)return; l.title=title.slice(0,150);if(state.current===lid)$('readerTitle').textContent=l.title;save();renderLibrary();toast('تم تعديل اسم الدرس')}",
    "function editLessonTitle(lid){const l=state.lessons.find(x=>x.id===lid);if(!l)return;appPrompt('تعديل اسم الدرس','الاسم الجديد:',l.title).then(next=>{if(next===null)return;const title=String(next).trim();if(!title)return;l.title=title.slice(0,150);if(state.current===lid&&$('readerTitle'))$('readerTitle').textContent=l.title;save();renderLibrary();toast('تم تعديل اسم الدرس')})}",
    "editLessonTitle",
)

once(
    "function deleteLesson(lid){const l=state.lessons.find(x=>x.id===lid);if(!l)return;if(!confirm('حذف هذا الدرس نهائيًا؟\\n'+l.title))return;dictionaryOccurrenceIndexCache=null;storageMutationIntent={type:'delete-lesson',removedLessonIds:[String(lid)]};state.lessons=state.lessons.filter(x=>x.id!==lid);if(state.current===lid){state.current=null;showPage('library')}save();renderAll();toast('تم حذف الدرس')}",
    "function deleteLesson(lid){const l=state.lessons.find(x=>x.id===lid);if(!l)return;appConfirm('حذف الدرس','حذف هذا الدرس نهائيًا؟\\n'+l.title).then(ok=>{if(!ok)return;dictionaryOccurrenceIndexCache=null;storageMutationIntent={type:'delete-lesson',removedLessonIds:[String(lid)]};state.lessons=state.lessons.filter(x=>x.id!==lid);if(state.current===lid){state.current=null;showPage('library')}save();renderAll();toast('تم حذف الدرس')})}",
    "deleteLesson",
)

once(
    "function resetSettingsToDefault(){if(!confirm('إعادة إعدادات الواجهة إلى القيم الافتراضية؟\\nلن يتم حذف الدروس أو الكلمات أو المشاريع.'))return;state.settings={...DEFAULT_SETTINGS};syncSettings();save(true);toast('تمت إعادة إعدادات النظام الافتراضية')}",
    "function resetSettingsToDefault(){appConfirm('إعادة الإعدادات','إعادة إعدادات الواجهة إلى القيم الافتراضية؟\\nلن يتم حذف الدروس أو الكلمات أو المشاريع.').then(ok=>{if(!ok)return;state.settings={...DEFAULT_SETTINGS};syncSettings();save(true);toast('تمت إعادة إعدادات النظام الافتراضية')})}",
    "resetSettings",
)

# clearAllAppData uses two confirms — replace those two lines
once(
    "  if(!confirm(message))return;\n  if(!confirm('حماية إضافية: سيتم أولًا حفظ الحالة الحالية والتحقق منها، ثم إنشاء نسخة استرجاع داخل التخزين، وبعدها فقط ستتم تهيئة التطبيق. هل تريد المتابعة؟'))return;",
    """  const ok1=await appConfirm('تحذير نهائي',message);if(!ok1)return;
  const ok2=await appConfirm('حماية إضافية','سيتم أولًا حفظ الحالة الحالية والتحقق منها، ثم إنشاء نسخة استرجاع داخل التخزين، وبعدها فقط ستتم تهيئة التطبيق. هل تريد المتابعة؟');if(!ok2)return;""",
    "clearAll-confirms",
)

once(
    """function moveLessonToProject(lid){const l=state.lessons.find(x=>x.id===lid);if(!l)return;const choices=['0|بدون مشروع',...state.projects.map(p=>`${p.id}|${p.name}`)];const current=l.projectId||'';const message='أدخل رقم المشروع:\\n\\n'+choices.map((x,i)=>`${i}. ${x.split('|')[1]}`).join('\\n')+'\\n\\nرقم 0 = بدون مشروع';const raw=prompt(message,String(Math.max(0,choices.findIndex(x=>x.startsWith((current||'0')+'|')))));if(raw===null)return;const n=Number(raw);if(!Number.isInteger(n)||n<0||n>=choices.length){toast('اختيار غير صالح');return}const chosen=choices[n].split('|')[0];l.projectId=chosen==='0'?'':chosen;save();renderAll();toast(l.projectId?'تم نقل الدرس إلى المشروع':'تم إخراج الدرس من المشروع')}""",
    """function moveLessonToProject(lid){const l=state.lessons.find(x=>x.id===lid);if(!l)return;const options=[{value:'',label:'بدون مشروع'},...state.projects.map(p=>({value:p.id,label:p.name}))];appSelect('نقل الدرس','اختر المشروع الذي سيُنقل إليه «'+l.title+'»',options,l.projectId||'').then(chosen=>{if(chosen===null||chosen===false)return;l.projectId=chosen||'';save();renderAll();toast(l.projectId?'تم نقل الدرس إلى المشروع':'أصبح الدرس في مجلد «دروس بدون مشروع»')})}""",
    "moveLessonToProject",
)

# word delete confirm in bind()
once(
    "if(confirm('مسح هذه الكلمة من الذاكرة؟')){delete state.words[wd.dataset.wordDelete];invalidateWordStatusCaches();save();renderAll();toast('تم مسح الكلمة من الذاكرة')}",
    "appConfirm('مسح الكلمة','مسح هذه الكلمة من الذاكرة؟').then(ok=>{if(!ok)return;delete state.words[wd.dataset.wordDelete];invalidateWordStatusCaches();save();renderAll();toast('تم مسح الكلمة من الذاكرة')})",
    "word-delete-confirm",
)

# ---------------------------------------------------------------------------
# 13. bind dialog buttons + gemini test + backups + model select
# ---------------------------------------------------------------------------
once(
    "loadGeminiKey();saveGeminiConfig();updateGeminiSourceStats();",
    """loadGeminiKey();saveGeminiConfig();syncGeminiUi();updateGeminiSourceStats();
safeBind('geminiTestBtn','onclick',testGeminiModel);
safeBind('geminiModel','onchange',()=>{const cfg=getGeminiConfig();cfg.model=$('geminiModel').value;try{localStorage.setItem(GEMINI_CONFIG_STORAGE,JSON.stringify(cfg))}catch(e){}toast('تم اعتماد النموذج')});
safeBind('refreshBackupsBtn','onclick',renderBackupList);
safeBind('appDialogOk','onclick',()=>{
  const mode=$('appDialogInput')?.hidden===false?'prompt':($('appDialogSelect')?.hidden===false?'select':'confirm');
  if(mode==='prompt')closeAppDialog($('appDialogInput').value);
  else if(mode==='select')closeAppDialog($('appDialogSelect').value);
  else closeAppDialog(true);
});
safeBind('appDialogCancel','onclick',()=>closeAppDialog(false));
safeBind('appDialogClose','onclick',()=>closeAppDialog(false));
$('appDialogInput')?.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();closeAppDialog($('appDialogInput').value)}if(e.key==='Escape')closeAppDialog(false)});
""",
    "bind-new-controls",
)

# ---------------------------------------------------------------------------
# 14. Gemini UI sync helper + backup restore (before boot)
# ---------------------------------------------------------------------------
once(
    "function loadGeminiKey(){",
    """function syncGeminiUi(){
  try{
    const cfg=getGeminiConfig();
    if($('geminiModel') && [...$('geminiModel').options].some(o=>o.value===cfg.model))$('geminiModel').value=cfg.model;
  }catch(e){}
}
async function listPersistentBackups(){
  try{
    const db=await idbOpen();
    return await new Promise((res,rej)=>{
      const tx=db.transaction(DB_BACKUP_STORE,'readonly');
      const store=tx.objectStore(DB_BACKUP_STORE);
      const req=store.getAll(), keysReq=store.getAllKeys();
      let values=null,keys=null;
      const finish=()=>{if(values&&keys)res(values.map((value,i)=>({value,key:String(keys[i]),savedAt:Number(value?._storage?.savedAt||value?.updatedAt)||0,lessons:Array.isArray(value?.lessons)?value.lessons.length:0,revision:extractRecordRevision(value)})))};
      req.onsuccess=()=>{values=req.result||[];finish()};
      keysReq.onsuccess=()=>{keys=keysReq.result||[];finish()};
      req.onerror=()=>rej(req.error||new Error('backup_list_failed'));
      keysReq.onerror=()=>rej(keysReq.error||new Error('backup_keys_failed'));
    });
  }catch(e){console.warn('list backups',e);return []}
}
async function renderBackupList(){
  const host=$('backupList');if(!host)return;
  host.innerHTML='<div class="settings-note">جارٍ قراءة النسخ…</div>';
  const items=await listPersistentBackups();
  items.sort((a,b)=>b.savedAt-a.savedAt);
  if(!items.length){host.innerHTML='<div class="settings-note">لا توجد نسخ استرجاع بعد. ستُنشأ تلقائيًا عند الحفظ الآمن أو الاستيراد أو المسح.</div>';return;}
  host.innerHTML=items.slice(0,12).map(x=>{
    const when=x.savedAt?new Date(x.savedAt).toLocaleString('ar-EG'):'بدون تاريخ';
    return `<div class="backup-row"><div><b>${esc(String(x.key))}</b><span>${esc(when)} · ${x.lessons} درس</span></div><button class="mini" data-restore-backup="${esc(x.key)}" type="button">استرجاع</button></div>`;
  }).join('');
}
async function restorePersistentBackup(key){
  const ok=await appConfirm('استرجاع نسخة','سيتم استبدال الحالة الحالية بهذه النسخة. الحالة الحالية تُحفظ كنسخة احتياطية أولًا إن أمكن.');
  if(!ok)return;
  try{
    const db=await idbOpen();
    const record=await new Promise((res,rej)=>{const tx=db.transaction(DB_BACKUP_STORE,'readonly');const req=tx.objectStore(DB_BACKUP_STORE).get(key);req.onsuccess=()=>res(req.result||null);req.onerror=()=>rej(req.error||new Error('backup_read_failed'))});
    if(!record||typeof record!=='object'){toast('تعذر قراءة هذه النسخة');return}
    if(!(await verifyStorageRecord(record))){toast('بصمة النسخة غير مطابقة؛ لم يتم الاسترجاع');return}
    await createPersistentBackup(snapshot(storageRevision),'before_restore');
    storageMutationIntent={type:'restore-backup',allowAllLessonRemoval:true,reason:'explicit-user-restore'};
    if(!loadStateData(record)){toast('تعذر تحميل النسخة');return}
    storageRevision=Number(record.revision)||Number(record.updatedAt)||nextStorageRevision();
    const saved=await saveNow(true);
    if(!saved){toast('حُمّلت النسخة في الذاكرة لكن تعذر تثبيتها في التخزين');renderAll();return}
    renderAll();syncSettings();showPage('library');toast('تم استرجاع النسخة بنجاح');
  }catch(e){console.warn(e);toast('فشل الاسترجاع: '+(e?.message||e))}
}
function loadGeminiKey(){""",
    "backup-restore-fns",
)

# click handler for restore backup buttons — add in the big click listener
once(
    "const cp=e.target.closest('[data-create-project]');if(cp){e.stopPropagation();createProject();return}",
    "const rb=e.target.closest('[data-restore-backup]');if(rb){e.stopPropagation();restorePersistentBackup(rb.dataset.restoreBackup);return}const cp=e.target.closest('[data-create-project]');if(cp){e.stopPropagation();createProject();return}",
    "restore-click",
)

# render backups when opening settings
once(
    "if(page==='settings'){syncSettings();renderSettingsDashboard();}",
    "if(page==='settings'){syncSettings();renderSettingsDashboard();renderBackupList();}",
    "settings-render-backups",
)

# quota in storage health
once(
    "el.dataset.state=(dbOk&&storageHealth.lastSaveSource)?'ok':'warn'}catch(e){console.warn('Storage health UI failed:',e)}}",
    """el.dataset.state=(dbOk&&storageHealth.lastSaveSource)?'ok':'warn';
    try{if(navigator.storage?.estimate){const est=await navigator.storage.estimate();const used=est.usage||0,quota=est.quota||0;if(quota){const pct=Math.round(used/quota*100);el.textContent+=(pct>=80?` · ⚠ امتلاء التخزين ${pct}%`:` · استخدام التخزين ${pct}%`);if(pct>=80)el.dataset.state='warn'}}}catch(e2){}
  }catch(e){console.warn('Storage health UI failed:',e)}}""",
    "storage-quota",
)

# ---------------------------------------------------------------------------
# 15. hideSplash defined before use; skip SW inside iframe; drop netlify observer
# ---------------------------------------------------------------------------
once(
    "boot().then(hideSplash).catch(hideSplash);\n})();",
    """boot().then(()=>window.hideSplash&&window.hideSplash()).catch(err=>{
  console.error('Lingo boot failed',err);
  const box=$('bootError');
  if(box){box.textContent='تعذر بدء التطبيق: '+(err&&err.message||err)+' — بياناتك لم تُمس. أعد التحميل أو استرجع نسخة من الإعدادات.';box.classList.add('show')}
  window.hideSplash&&window.hideSplash();
});
})();""",
    "boot-catch",
)

once(
    """<script>
if('serviceWorker' in navigator){window.addEventListener('load',()=>{navigator.serviceWorker.register('./sw.js').catch(()=>{});});}
const _splashStart=Date.now();
function hideSplash(){
  const el=document.getElementById('lingoSplash');if(!el)return;
  const minShow=900,elapsed=Date.now()-_splashStart,wait=Math.max(0,minShow-elapsed);
  setTimeout(()=>{el.classList.add('splash-out');setTimeout(()=>el.remove(),520);},wait);
}
setTimeout(hideSplash,4000); /* safety fallback in case boot() never resolves */
</script>

<!-- حذف شريط Netlify بشكل ديناميكي -->
<script>
  window.addEventListener('load', () => {
    // حذف أي عنصر Netlify موجود
    document.querySelectorAll('[class*="netlify"], [id*="netlify"], iframe[src*="netlify"]').forEach(el => {
      el.style.display = 'none';
      el.style.visibility = 'hidden';
      el.remove();
    });
  });
  
  // مراقبة مستمرة لأي عناصر Netlify جديدة
  const observer = new MutationObserver(() => {
    document.querySelectorAll('[class*="netlify"], [id*="netlify"]').forEach(el => {
      el.remove();
    });
  });
  
  observer.observe(document.body, { childList: true, subtree: true });
</script>""",
    """<script>
window.hideSplash=function hideSplash(){
  const el=document.getElementById('lingoSplash');if(!el)return;
  const minShow=700,elapsed=Date.now()-(window._splashStart||Date.now()),wait=Math.max(0,minShow-elapsed);
  setTimeout(()=>{el.classList.add('splash-out');setTimeout(()=>el.remove(),480);},wait);
};
window._splashStart=Date.now();
if('serviceWorker' in navigator && window.top===window.self){
  window.addEventListener('load',()=>{navigator.serviceWorker.register('./sw.js').catch(()=>{});});
}
setTimeout(()=>window.hideSplash&&window.hideSplash(),5000);
</script>""",
    "splash-sw-netlify",
)

# Also define hideSplash early so boot can call it even if later script is slow
once(
    "(function(){\n  const MIN_BOTTOM_RESERVE=64;",
    """window._splashStart=Date.now();
window.hideSplash=window.hideSplash||function(){const el=document.getElementById('lingoSplash');if(!el)return;el.classList.add('splash-out');setTimeout(()=>el.remove(),480)};
(function(){
  const MIN_BOTTOM_RESERVE=64;""",
    "early-hidesplash",
)

# ---------------------------------------------------------------------------
# 16. showPage: don't crash if a helper throws
# ---------------------------------------------------------------------------
once(
    "if(page==='library')renderLibrary();if(page==='translate'){renderProjectUI();updateTranslationProviderUI()}if(page==='dictionary'){renderDictionary();}if(page==='words')renderWords();if(page==='stats')renderStats();if(page==='settings'){syncSettings();renderSettingsDashboard();renderBackupList();}if(page!=='reader'){closeWordPopup();closeReaderTools()}",
    """try{
    if(page==='library')renderLibrary();
    if(page==='translate'){renderProjectUI();if(typeof updateTranslationProviderUI==='function')updateTranslationProviderUI();syncGeminiUi();}
    if(page==='dictionary')renderDictionary();
    if(page==='words')renderWords();
    if(page==='stats')renderStats();
    if(page==='settings'){syncSettings();renderSettingsDashboard();renderBackupList();}
    if(page!=='reader'){closeWordPopup();closeReaderTools()}
  }catch(err){console.warn('showPage render',err);toast('تعذر تحديث هذه الشاشة بالكامل، لكن التنقل يعمل.')}""",
    "showPage-try",
)

# topTitle null-safe
once(
    "$('topTitle').textContent=title;",
    "if($('topTitle'))$('topTitle').textContent=title;",
    "topTitle-null",
)

DST.write_text(html, encoding="utf-8")
print("WROTE", DST, "bytes", DST.stat().st_size)
print("join leftover \\\\n", html.count("join('\\\\n')"))
print("updateTranslationProviderUI defs", html.count("function updateTranslationProviderUI"))
print("hideSplash window", html.count("window.hideSplash"))
print("appDialog", html.count("id=\"appDialog\""))
print("geminiModel", html.count("id=\"geminiModel\""))
print("backupList", html.count("id=\"backupList\""))
print("__unassigned__", html.count("__unassigned__"))
