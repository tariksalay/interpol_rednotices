# **Interpol Red Notices Web Application**

## **Introduction**
This Dockerized project fetches data from Interpol's wanted list using a Python app. Periodically, the retrieved red notices are stored in a message queue system and then consumed by a web server. The server saves the data into a database and displays it on a web page, timestamped. The architecture involves three Docker containers, facilitating seamless operation and scalability.

## **Project Structure**
- app/
	- Container_A
		- Dockerfile
		- producer.py
		- reqs.txt
		- scraper.py
	- Container_B
		- consumer.py
		- db.py
		- Dockerfile
- flask.py
- reqs.txt
	- Container_C
		- Dockerfile
		- reqs.txt


## **Architecture**
The application is composed of three Docker containers:

1. **'Container A'**: This container retrieves the data from the Interpol’s website and pulls red notices and puts it into the message queue system in Container C.

2. **'Container B'**: The Python-based web server in this container actively monitors the message queue system hosted in Container C. Upon receiving new data, it securely stores it in the designated database and promptly showcases it on a straightforward HTML web page, accompanied by a timestamp. Real-time updates on the web page occur whenever fresh data is fetched from the queue. Moreover, should an existing record undergo modification, the web page promptly alerts users with an alarm notification.

3. **'Container C'**: This container consists of the messages passed by message queue system RabbitMQ.


## **Documentation**

* **'reqs.txt'**: Text file that contains a list of Python library dependencies required to run the application
* **'scraper_producer.py'**: Python script that scrapes data from Interpol and pushes to a declare message queue
* **'definition.html'**: HTML file to structure the content of the web page
* **'consumer_db.py'**: Python script that consumes the message from queue and stores it on Postgres database
* **'pg_hba.py'**: PostgreSQL client authentication configuration file
* **'start_app.sh'**: Shell script to start Postgres database
* **'webapp.py'**: Python script to publish the stored data on a web application
* **'docker-compose.yml'**: The Docker Compose configuration to define and manage multi-container application, in a YAML file.
* **'README.md'**: Th text file describing this project


## **Extra: Topics to Cover**

* **'Scraper (Selenium)'**
* **'Producer (RabbitMQ)'**
* **'Consumer (RabbitMQ)'**
* **'Database (PostgreSQL) '**
* **'Web App (Flask)'**
* **'HTML'**
* **'Containerize (Docker)'**
* **'Version-Control (Git)'**
* **'Docker Containers: A (Scraper + Producer) -> C (RabbitMQ) -> B (Consumer + DB + Web App)'**

# **This task in Turkish:**

## **Görev Konusu**
Bu görevde,  Interpol tarafından yayınlanan arananlar verisi çekilir ve kuyruğa yazılır. Kuyruktan okunan bu bilgiler veritabanına kayıt edilir ve bir web server üzerinden paylaşılır. Uygulama aşağıda belirtilen mimaride yapılmalıdır.
Tüm işlemler kullanıcıya görsel bir arayüz ile sunulmalı ve docker ortamına uygun şekilde hazırlanmalıdır.

## **Gerekli Maddeler**:
* **'Container A'**: Mimari 3 container'dan oluşmaktadır. Belirli bir periyot süre ile sürekli olarak “Interpol” tarafından yayınlanan kırmızı liste verisi çekilir ve Container C'de bulunan kuyruk sistemine aktarılır 
* **'Container B'**: Python ile hazırlanmış bir web sunucu olmalıdır. Burada Container C de bulunan kuyruk dinlenmelidir. Kuyruktan elde edilen bilgiler istenilen veritabanında kaydedilmelidir. Bu bilgiler web sunucu ile basit bir html web sayfasında zaman bilgisi ile birlikte gösterilmelidir. Kuyruktan elde edilen her bilgi web sunucunun paylaştığı arayüz sayfası güncellenmelidir. Önceden kayıt edilmiş bilgilerin güncellenmesi durumu ise alarm olarak arayüzde gösterilmelidir.
* **'Container C '**: Bir mesaj kuyruğu sistemi olan “RabbitMQ” bulunmaktadır.
Yapıda değişkenlerin enviroment-config üzerinden müdahele edilebilir olması gerekmektedir (koda müdahale etmeden değişiklik yapılabilmeli),
Yapının Nesne Tabanlı Programlama temellerine göre oluşturulması,
İstenilen yazılım Docker ortamına uygun şekilde hazırlanmalıdır ve dockerize edilerek build ve deploy işlemleri yapılmalıdır. Docker-compose kullanılmalıdır,
Yazılım testleri, yazılımın çalışma gereksinimleri, yorumları ve detaylı açıklama dosyası gibi dokumantasyon ve kurulum yönergeleri hazırlanmalıdır. (requirements.txt, doc-test, readme.md, .dockerfile, vs.) 

## **Bilgilendirme**:
Görev süresince python programlama dili kullanılmalıdır.
Her türlü açık kaynaktan yararlanılabilir.
Sizden beklenilen, kullandığınız/yazdığınız kodları anlamanız ve açıklamanızdır.
Gerekli maddelerin tamamının yapılamaması durumunda, yapılan maddelere göre değerlendirilme yapılacaktır.
Proje github yada gitlab ortamında geliştirilmelidir.
