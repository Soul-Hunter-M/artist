import os

image_dir = "images"
output = "index.html"

# 支持多种图片格式
images = sorted([
    f for f in os.listdir(image_dir)
    if f.lower().endswith((".png",".webp",".jpg",".jpeg"))
])

image_list = ",".join([f'"{i}"' for i in images])

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>画师合集</title>

<style>

body {{
margin:0;
background:#111;
color:white;
font-family:sans-serif;
}}

h1 {{
text-align:center;
padding:20px;
}}

#search {{
display:block;
margin:0 auto 20px auto;
padding:10px;
width:300px;
font-size:16px;
border-radius:6px;
border:none;
}}

.gallery {{
display:grid;
grid-template-columns:repeat(auto-fill,200px);
gap:15px;
padding:20px;
}}

.card {{
text-align:center;
}}

.card img {{
width:200px;
height:auto;
border-radius:6px;
cursor:pointer;
background:#222;
}}

.name {{
margin-top:5px;
font-size:14px;
color:#ccc;
word-break:break-all;
}}

.viewer {{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.95);
display:none;
justify-content:center;
align-items:center;
overflow:hidden;
}}

.viewer img {{
max-width:90%;
max-height:90%;
transition:transform 0.1s;
}}

</style>
</head>

<body>

<h1>画师合集</h1>

<input id="search" placeholder="搜索画师...">

<div class="gallery" id="gallery"></div>

<div class="viewer" id="viewer">
<img id="viewerImg">
</div>

<script>

const images = [{image_list}]

const gallery = document.getElementById("gallery")

images.forEach(name=>{{

const card=document.createElement("div")
card.className="card"

const img=document.createElement("img")

// 懒加载
img.dataset.src="images/"+name
img.loading="lazy"

img.onclick=()=>openViewer(img.dataset.src)

const label=document.createElement("div")
label.className="name"

// 去掉扩展名显示画师名
label.innerText=name.replace(/\\.[^/.]+$/, "")

card.appendChild(img)
card.appendChild(label)

gallery.appendChild(card)

}})


// 懒加载观察器
const lazyImages = document.querySelectorAll("img[data-src]")

const observer = new IntersectionObserver((entries, obs)=>{{
entries.forEach(entry=>{{

if(entry.isIntersecting){{

const img = entry.target
img.src = img.dataset.src
obs.unobserve(img)

}}

}})
}})

lazyImages.forEach(img=>observer.observe(img))


// 查看原图
const viewer=document.getElementById("viewer")
const viewerImg=document.getElementById("viewerImg")

let scale=1

function openViewer(src){{

viewer.style.display="flex"
viewerImg.src=src
scale=1
viewerImg.style.transform="scale(1)"

}}

viewer.onclick=()=>viewer.style.display="none"


// 滚轮缩放
viewerImg.onwheel=(e)=>{{

e.preventDefault()

if(e.deltaY<0){{
scale*=1.1
}}else{{
scale/=1.1
}}

viewerImg.style.transform="scale("+scale+")"

}}


// 搜索功能
document.getElementById("search").oninput=function(){{

const text=this.value.toLowerCase()

document.querySelectorAll(".card").forEach(card=>{{

const name=card.innerText.toLowerCase()

if(name.includes(text)){{
card.style.display=""
}}else{{
card.style.display="none"
}}

}})

}}

</script>

</body>
</html>
"""

with open(output,"w",encoding="utf-8") as f:
    f.write(html)

print("网站生成完成：index.html")