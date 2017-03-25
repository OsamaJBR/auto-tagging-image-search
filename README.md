# Search Images By Tagging Them
Tagging photos provides much better search capabilities, in this project I'm trying to build an intelligent way to search for images using image recognition (google-vision).

This project can be used as a back-end for backup solution, users only have to upload their images and its automatically gets tagged by google-vision services.

Also, it provides a translation capability, for example if translation for Arabic is enabled. Once the image got tags (labels) from google-vision service, all these tags will be translated using google-translation-api. So the user who is searching for 'مركبة' ( vehicle in Arabic) or the other who is looking for vehicle will get the same result. 

All these processes are done is async queue, as shown in How it works section, once the recognition and the translation process are done, a document for this image will be stored in ElasticSearch in the following structure : 

```
{
	"uploaded_at": "2017-03-25 08:54:15",
	"image_path": "/opt/personal/search-images-tags/datadir/flowers.jpg",
	"image_type": ".jpg",
	"timestamp": 1490428776,
	"en_lables": [
		"flower",
		"flora",
		"plant",
		"flower bouquet",
		"flower arranging",
		"floristry",
		"land plant",
		"petal",
		"macro photography",
		"flowering plant"
	],
	"image_fname": "flowers.jpg",
	"ar_lables": [
		"زهرة",
		"النباتية",
		"نبات",
		"باقة من الزهور",
		"ترتيب الزهور",
		"التزيين بالزهور",
		"نبات الأرض",
		"البتلة نبات",
		"تصوير الماكرو",
		"النباتات المزهرة"
	]
}
```
## How it works

![Alt text](/examples/tagging-images.png?raw=true "Optional Title")

## How to run 
1) Edit the config.ini file
2) Run the HTTP interface
```
$ python main.py
```
3) Run the Consumer Process
```
$ python consumer.py
```
4) Upload an image using CURL
```
$ curl -XPOST -F name=laptop.png -F data=@laptop.png http://127.0.0.1:5555/upload
```


## TO DO
* Add search for images to the bottle application
* Support different storage locations such (S3, Goolge Cloud Storage)
* Imporve search for arabic words (partial search) 
