from time import sleep
import cv2

tracker = cv2.TrackerKCF_create()
video = cv2.VideoCapture('test.mp4')


def video_frame_rescaled(video : cv2.VideoCapture,
                         width : int = 1280,
                         height : int = 720) -> tuple:
    ''' Returns next frame'''
    success, frame = video.read()

    if success:
        frame = cv2.resize(frame, (width, height))

    return success, frame


# Read at least first frame to select ROI for experimient
frame = None
while True:
    sucess, frame = video_frame_rescaled(video)

    cv2.imshow("Press esc to select frame for ROI select for tracking!",frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


while True:
    bbox = cv2.selectROI(frame, False)

    if (bbox is not None) or (bbox != (0, 0, 0, 0)):
        break


ok = tracker.init(frame, bbox)
cv2.destroyWindow("ROI selector")

while True:
    ok, frame = video_frame_rescaled(video)
    ok, bbox = tracker.update(frame)

    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]),
              int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,0,255), 2, 2)

    cv2.imshow("Tracking", frame)
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

