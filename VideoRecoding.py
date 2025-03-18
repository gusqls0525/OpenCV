import cv2 as cv

video = cv.VideoCapture("http://210.99.70.120:1935/live/cctv002.stream/playlist.m3u8")

codec = cv.VideoWriter_fourcc(*'mp4v')
videoWidth = int(video.get(3))
videoHeight = int(video.get(4))
recodingMode = False
nowRecoding = False
blackMode = False
number = 1
fps = 30
wait_msec = int(1 / fps * 1000)

if video.isOpened():
    
    while True:
        # video에서 이미지를 읽기
        valid, img = video.read()
        if not valid:
            break

        #흑백모드 적용
        if blackMode:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

        # 녹화된 프레임 따로, 출력용 프레임 따로
        displayImg = img.copy()
        recodingImg = img.copy()

        
        # 녹화모드 빨간테두리
        if nowRecoding:
            cv.rectangle(displayImg, (3,3), (videoWidth - 3, videoHeight - 3), (0,0,225), 3)
                
        # 현재 모드 창에서 표시
        if recodingMode:
            modeState = "Recoding Mode"
            cv.putText(displayImg, modeState, (10,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)      
        else:
            modeState = "Preview Mode"
            cv.putText(displayImg, modeState, (10,50), cv.FONT_HERSHEY_SIMPLEX, 1, (225,105,65), 2)      
                
        # 녹화
        if nowRecoding and recodedVideo is not None:
            recodedVideo.write(recodingImg)
            
        # 미리보기
        cv.imshow('CCTV in Cheonan', displayImg)
        
        key = cv.waitKey(wait_msec)
           
        # 스페이스 바로 모드 전환
        if key == ord(' '):
            recodingMode = not recodingMode
        # 흑백모드
        if key == ord('b'):
            blackMode = not blackMode
        # R키에 녹화버튼 할당
        if key == ord('r') and recodingMode:
            if nowRecoding: #녹화중인거 멈추고 저장
                recodedVideo.release()
                nowRecoding = False
                number += 1
            else: #녹화시작
                recodedVideo = cv.VideoWriter(f"CAcctv{number}.mp4", codec, fps, (videoWidth, videoHeight))
                nowRecoding = True
        
        # esc누르면 종료        
        if key == 27:
            break
            
    video.release()
    cv.destroyAllWindows()