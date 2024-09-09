
[models]

	- location.js : uid, loca_x, loca_y, loca_z, slope, chim_name, chim_num(같은 굴뚝(코스) 번호일때 1씩 증가하여 저장)

[routes]

	- index.js : mian 화면
 
	- *location.js : 모든 테스트 모여있는 곳 : (take off, save, arming)<mavSDK, (*Drone state check)<mavproxy
 
	- pyTest.js : 파이썬 연결 테스트. 지금은 안씀
 
	- pyTestt.js : 파이썬 테스트2
 
	- saveLocation.js: 좌표 저장 <mavSDK
 
	- socket_test.js: 콘솔 실시간 출력 테스트
 
	- user.js : 안쓰는곳

[views]

	- index.ejs
 
	- *location.ejs
 
	- moveDrone.ejs
 
	- pyTestt.ejs
 
	- saveLocation.ejs
 
	- selectChimny.ejs
 
	- socket_test.ejs

[pyCode]

	- drone_arming_test.py
 
	- drone_land_test.py
 
	- drone_save_test.py
 
	- *mavDroneTest.py : 드론 이동 코드 (아직 미완성)
 
	- *mavDroneTest2.py : 드론 
 
	- pytestt.py
 
	- saveLocation.py

<api>
	
/ : main
	
/location : 테스트 모음

/saveLocation : 좌표 추출 및 저장

/moveDrone : 좌표 이동



