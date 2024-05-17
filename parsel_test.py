import parsel

html_content = '''
<div class="detail detail-side">     
    <ul class="myui-vodlist__text col-pd clearfix">
		<li>
			<a href="/voddetail/129832.html" title="逆天邪神">
                <span class="pull-right  text-muted" style="color:;">30集全</span>            		<span class="badge badge-first">1</span>逆天邪神       
                </a>
		</li>
	</ul>
</div>
'''

selector1 = parsel.Selector(html_content)
a_selector = contents = selector1.css('.detail li')[0]
href = a_selector.css('a::attr(href)').get()
print(href)
text = a_selector.css('a::text').getall()
print(text)
print(a_selector.css('a::text').get())