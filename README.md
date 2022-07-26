# terjemah-epub
<em> Alat sederhana untuk menterjemahkan epub</em> <br>

## Installasi
  * Python3 <br>
  
  Windows
  ```
  python -m venv env
  env\Scripts\activate
  (env)> pip install -r requirements.txt 
  ```

  Linux
  ```
  python3 -m venv env
  source env\bin\activate
  (env)> pip install -r requirements.txt 
  ```
  
  ## Konfigurasi
  File: config.ini <br>
  Edit nilai <b>dst</b> untuk mengatur lokasi hasil terjemahan
  ```
  [Path]
  dst = /home/hafizd/Development/terjemah-epub/output
  ```
  ![1](https://user-images.githubusercontent.com/40784871/180902164-de74201e-7a37-40ac-9160-933da127da0b.png)
  
  ## Menjalankan 
  Windows 
  ```
  python main.py <path epub>
  ```
 
  Linux
  ```
  python3 main.py <path epub>
  ```
  
  ![2](https://user-images.githubusercontent.com/40784871/180903107-7f4b1c13-ca40-4efa-8007-44afd85472b5.png)
  
  
  ## Output
  Original
  ![3](https://user-images.githubusercontent.com/40784871/180905142-543bdb62-c380-4d87-bef3-df7d1e9fb14b.png)

  Translated
  ![4](https://user-images.githubusercontent.com/40784871/180905153-6c3f4712-ba0e-40c6-982b-d2af56fac27a.png)


