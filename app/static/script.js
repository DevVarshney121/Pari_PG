const $=(s,p=document)=>p.querySelector(s), $$=(s,p=document)=>[...p.querySelectorAll(s)];
const navToggle=$("#navToggle"), mainNav=$("#mainNav");
navToggle?.addEventListener("click",()=>{const open=mainNav.classList.toggle("open");navToggle.setAttribute("aria-expanded",open)});
$$(".main-nav a").forEach(a=>a.addEventListener("click",()=>mainNav.classList.remove("open")));

const modal=$("#roomModal");
function openRoom(data){
  $("#modalImage").src=data.image; $("#modalImage").alt=data.title;
  $("#modalTitle").textContent=data.title; $("#modalPrice").textContent=data.price+" / month";
  $("#modalBadge").textContent=data.tag; $("#modalDescription").textContent=data.description;
  $("#modalMeta").innerHTML=(data.meta||[]).map(x=>`<div>✓ ${String(x).trim()}</div>`).join("");
  $("#modalFeatures").innerHTML=(data.features||[]).map(x=>`<span>✓ ${String(x).trim()}</span>`).join("");
  modal.classList.add("show");modal.setAttribute("aria-hidden","false");document.body.style.overflow="hidden";
}
function closeRoom(){modal.classList.remove("show");modal.setAttribute("aria-hidden","true");document.body.style.overflow=""}
$$(".details").forEach(btn=>btn.addEventListener("click",()=>openRoom(JSON.parse(btn.dataset.room))));
$("#modalClose")?.addEventListener("click",closeRoom);
$(".modal-backdrop")?.addEventListener("click",closeRoom);
document.addEventListener("keydown",e=>{if(e.key==="Escape")closeRoom()});
$("#modalBook")?.addEventListener("click",closeRoom);

const filterType=$("#filterType"), roomsGrid=$("#roomsGrid");
$("#checkAvailability")?.addEventListener("click",()=>{
 const type=filterType.value;
 $$(".room-card",roomsGrid).forEach(card=>card.style.display=(type==="all"||card.dataset.type===type)?"":"none");
 $("#rooms").scrollIntoView({behavior:"smooth"});
 showToast("Room availability list updated.");
});
$("#viewAllRooms")?.addEventListener("click",()=>{$$(".room-card",roomsGrid).forEach(c=>c.style.display="");showToast("Showing all room types.");});

$$(".faq-question").forEach(btn=>btn.addEventListener("click",()=>btn.parentElement.classList.toggle("open")));
$$(".gallery-img").forEach(img=>img.addEventListener("click",()=>window.open(img.src,"_blank","noopener")));

const form=$("#contactForm"), status=$("#formStatus"), submit=$("#contactSubmit");
form?.addEventListener("submit",async e=>{
 e.preventDefault();status.textContent="";status.className="form-status";submit.disabled=true;submit.textContent="Sending...";
 try{
   const res=await fetch("/api/contact",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
   const data=await res.json();
   if(!res.ok||!data.success) throw new Error(data.message||"Unable to submit.");
   status.textContent=data.message;status.classList.add("success");form.reset();showToast("Message submitted successfully.");
 }catch(err){status.textContent=err.message;status.classList.add("error")}
 finally{submit.disabled=false;submit.textContent="➤ Send Message"}
});

const toTop=$("#toTop");
window.addEventListener("scroll",()=>{
 toTop.style.display=scrollY>450?"grid":"none";
 const sections=$$("main section[id]");
 let current="home";
 sections.forEach(s=>{if(s.getBoundingClientRect().top<=110)current=s.id});
 $$(".main-nav a").forEach(a=>a.classList.toggle("active",a.getAttribute("href")==="#"+current));
});
toTop?.addEventListener("click",()=>scrollTo({top:0,behavior:"smooth"}));

function showToast(msg){const t=$("#toast");t.textContent=msg;t.classList.add("show");clearTimeout(window.toastTimer);window.toastTimer=setTimeout(()=>t.classList.remove("show"),2200)}
