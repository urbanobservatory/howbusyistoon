---
menu: "navigation"
title: "How busy is it?"
weight: 1
layout: page
colour: "blue"
header: "Use How Busy Is… to help you find information to safely and confidently visit your city centre. "
headerhighlight: ""
callout: "{{ header }} {{ headerhighlight }}"
---
{{< rawhtml >}}
<p>To see what your city centre is like right now, check out our webcams below. They’re located on Northumberland Street and Grey Street and they update a still image of the video feed approximately every 5 minutes.</p>
<h2>Northumberland Street</h2>
<div class="videoWrapper"><img :src="videoImage1" /></div>
<h2>Grey Street</h2>
<div class="videoWrapper"><img :src="videoImage2" /></div>
<p>Images from webcams update approximately every 5 minutes.</p>
{{< /rawhtml >}}
