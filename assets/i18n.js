/* Shared portfolio language handling. Explicit URLs retain language across reloads. */
(() => {
 const vi=location.pathname.startsWith('/vi/');
 const dictionary=window.SITE_VI||{};
 const translate=value=>dictionary[value]||value;
 window.localizePage=()=>{
  document.documentElement.lang=vi?'vi':'en';
  document.querySelectorAll('[data-language]').forEach(link=>{
   const target=link.dataset.language;
   link.href=(target==='vi'?'/vi/':'/')+location.hash;
   if((target==='vi')===vi)link.setAttribute('aria-current','true');else link.removeAttribute('aria-current');
  });
  if(!vi)return;
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
  nodes.forEach(node=>{if(node.parentElement.closest('script,style'))return;const s=node.nodeValue.trim(),t=translate(s);if(t!==s)node.nodeValue=node.nodeValue.replace(s,t)});
  document.querySelectorAll('[alt],[aria-label],[placeholder],[data-certificate-title]').forEach(el=>{
   ['alt','aria-label','placeholder','data-certificate-title'].forEach(attr=>{if(el.hasAttribute(attr))el.setAttribute(attr,translate(el.getAttribute(attr)))});
  });
  document.querySelectorAll('a[href]').forEach(a=>{if(a.hasAttribute('data-language'))return;const href=a.getAttribute('href');if(href.startsWith('#'))a.setAttribute('href','/vi/'+href);else if(href==='/'||href.startsWith('/blog/'))a.setAttribute('href','/vi'+href)});
 };
})();
