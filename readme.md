Python3을 사용해서 ‘인터파크 티켓팅’하는 프로그램을 만들거야. 사용자에게 GUI를 제공하여 예매할 수 있도록 코드 산출물은 실행파일(windows, mac 둘 다)로 나와야 해. 코드를 알려줘.

1. 프로그램 실행 시 사용자에게 아래 input을 입력받는 gui 화면 제공.
1-1. 콘서트 ID 입력 (only numbers)
1-2. 티켓 개수 입력 (1~4까지의 숫자)
1-3. 원하는 날짜 (e.g. 4/18일 콘서트의 경우, 사용자는 숫자 18 입력)
1-4. 인터파크티켓 ID
1-5. 인터파크티켓 PW
1-6. 사용자가 GUI의 'Start'버튼을 누를 시 아래 2번 단계를 수행.

2. 1-4, 1-5 에서 입력받은 아이디와 패스워드를 사용해 아래 페이지에서 로그인을 수행.
* page url : "https://ticket.interpark.com/Gate/TPLogin.asp"
2-1. ID입력란은 위 페이지의 html 파일에서 <div class="inputStyle inputId"><label><input value="" autofocus="" type="text" class="inputText id" name="userId" id="userId" placeholder="아이디”></label></div> 로 되어있어.
2-2. PW입력란은 <div class="inputStyle inputPw"><label><input type="password" class="inputText pw" name="userPwd" id="userPwd" placeholder="비밀번호”></label></div> 로 되어있어.
2-3. 로그인 버튼은 <button type="button" class="loginBtn" id="btn_login" onclick=javascript:gtm_eventTag('user_interaction', 'click', '로그인 진행’, ‘’, ‘로그인’,‘button','','',);"> 으로 되어있어.
2-4. 로그인 버튼을 눌러 로그인을 시도해.
2-5. 로그인 실패할 경우, 사용자가 직접 id/pw를 입력해 로그인하도록 하고, 로그인 성공 시 이동되는 3번 단계의 페이지를 기다리도록 함.
2-6. 로그인 성공할 경우, 아래 3번 단계의 페이지로 이동.

3. 인터파크 메인 페이지(https://tickets.interpark.com)에서 “로그인 된 상태를 유지”하며 아래 내용을 수행해야해.
3-1. 1-1에서 입력받은 콘서트 아이디를(targetConcertId) 기반으로 아래 url로 이동해.
"https://tickets.interpark.com/goods/targetConcertId"
3-2. 페이지 이동 후 발생하는 팝업창을 모두 닫아줘. 3-1 페이지에서 팝업창은 <div class="popupWrap"> 태그로 이루어져있고, 닫기 버튼은 <button class="popupCloseBtn"> 으로 되어있어.
3-3. 3-1페이지에서, 1-3에서 입력받은 날짜(wantedDate)에 해당되는 버튼을 클릭해. <div class="datepicker><div class="datepicker-container datepicker-inline"><div class="datepicker-panel" data-view="days picker"><ul>...</ul><ul data-view="week">...</ul><ul data-view="days"><li class="muted">0</li><li class="disabled">1</li><li class="picked">16</li><li class>18></li></ul></div> 로 되어있어.
* li 태그의 disabled 클래스는 여러개가 존재할 수 있고, picked class는 1개 혹은 0개 존재할 수 있어. class가 지정이 안 된 날짜(18일의 경우)도 존재할 수 있어.
3-4. 예매하기 버튼을 클릭해서 4번 창으로 이동해. 이 때, 예매하기 버튼은 아래처럼 태그 구성이 되어있어.
<a class="sideBtn is-primary" href="#" data-check="false"><span>예매하기</span></a>

4. 대기열이 많은 경우, 4번의 ’새 창‘에서 4-1화면이 나타나기까지 시간이 오래 걸릴 수 있어. 세션이 끊어지지 않도록 하고, 페이지에서 “잠깐 접어두기”버튼이 로딩되는 걸 기다렸다가 버튼을 클릭해. 해당 버튼은 아래 태그로 구성되어 있어.
<div id="divCaptchaFolding" class="captchaFolding">"좌석 보고 입력하려면,“<a href="javascript::" onclick=capchaHide()">잠깐 접어두기&nbsp;&nbsp;</a></div>

4-1. 사용자가 4의 화면에서 마우스 클릭을 할 때까지 기다리고, 다음 화면(4-2) 로딩을 기다려.
4-2. 화면이 정상적으로 로딩될 경우 html에서 좌석배치도입니다 라는 문자열이 존재해. <b><font>...</font>"의 좌석배치도입니다.“</b>
위 태그가 로딩될때까지 기다려.
4-3. 로딩된 4-2의 화면에서 아래 내용을 수행해.
4-3-1. <span class="SeatR"</span>
4-3-2. <span class="SeatB"</span>
4-3-3. <span class="SeatN"</span>
SeatR, SeatB, SeatN은 모두 2개 이상 존재해. 태그를 ’순차적으로 순회‘하면서 1-2번에서 입력받은 개수만큼 SeatN을 클릭해. SeatB와 SeatR은 무시하도록 해.
4-4. <a href="javascript:fnSelect();"><img id=NextStepImage" alt="좌석선택완료”></a> 태그로 구성되어 있는 이미지를 클릭해.
4-5. 팝업창으로 아래 태그의 input영역을 클릭해서 활성화시켜줘.
<input type="text" id="textCaptcha" name="txtCaptcha" onKeyDown="IsEnterGo();">

