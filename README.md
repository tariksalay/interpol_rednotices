Görev Konusu :
Bu görevde,  Interpol tarafından yayınlanan arananlar verisi çekilir ve kuyruğa yazılır. Kuyruktan okunan bu bilgiler veritabanına kayıt edilir ve bir web server üzerinden paylaşılır. Uygulama aşağıda belirtilen mimaride yapılmalıdır.
Tüm işlemler kullanıcıya görsel bir arayüz ile sunulmalı ve docker ortamına uygun şekilde hazırlanmalıdır.

Gerekli Maddeler:
•	Mimari 3 container'dan oluşmaktadır. 
◦ Container A: Belirli bir periyot süre ile sürekli olarak “Interpol” tarafından yayınlanan kırmızı liste verisi çekilir ve Container C'de bulunan kuyruk sistemine aktarılır.
◦ Container B: Python ile hazırlanmış bir web sunucu olmalıdır. Burada Container C de bulunan kuyruk dinlenmelidir. Kuyruktan elde edilen bilgiler istenilen veritabanında kaydedilmelidir. Bu bilgiler web sunucu ile basit bir html web sayfasında zaman bilgisi ile birlikte gösterilmelidir. Kuyruktan elde edilen her bilgi web sunucunun paylaştığı arayüz sayfası güncellenmelidir. Önceden kayıt edilmiş bilgilerin güncellenmesi durumu ise alarm olarak arayüzde gösterilmelidir.
◦ Container C: Bir mesaj kuyruğu sistemi olan “RabbitMQ” bulunmaktadır.
•	Yapıda değişkenlerin enviroment-config üzerinden müdahele edilebilir olması gerekmektedir (koda müdahale etmeden değişiklik yapılabilmeli),
•	Yapının Nesne Tabanlı Programlama temellerine göre oluşturulması,
•	İstenilen yazılım Docker ortamına uygun şekilde hazırlanmalıdır ve dockerize edilerek build ve deploy işlemleri yapılmalıdır. Docker-compose kullanılmalıdır,
•	Yazılım testleri, yazılımın çalışma gereksinimleri, yorumları ve detaylı açıklama dosyası gibi dokumantasyon ve kurulum yönergeleri hazırlanmalıdır(requirements.txt, doc-test, readme.md, .dockerfile, vs.) .

Bilgilendirme:
•	Görev süresince python programlama dili kullanılmalıdır.
•	Her türlü açık kaynaktan yararlanılabilir.
•	Sizden beklenilen, kullandığınız/yazdığınız kodları anlamanız ve açıklamanızdır.
•	Gerekli maddelerin tamamının yapılamaması durumunda, yapılan maddelere göre değerlendirilme yapılacaktır.
•	Proje github yada gitlab ortamında geliştirilmelidir.



Topics to cover:
1 - Scrape (Selenium) 
2 - Amqp (Rabbitmq)
3 - Database (Postgresql)
4 - Web App (Flask)
5 - Containerize (Docker)
6 - Version-Control (Git)

Docker Containers: 
A -> C -> B 
A - (Scraper + Producer)
B - (Consumer + DB + Web App)
C - (Rabbitmq)
