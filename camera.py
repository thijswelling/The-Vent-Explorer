import cv2
import numpy


class Camera:
    def __init__(self, camId: int = 0, resolution: tuple[int, int] = (1280, 720)):
        self.cam = cv2.VideoCapture(camId)
        self.resolution = resolution
        self.cam.set(3, resolution[0])
        self.cam.set(4, resolution[1])

    def get_image(self, show=False):
        ret, frame = self.cam.read()
        frame = frame if ret else numpy.zeros(self.resolution)
        if show:
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
        return frame

    def release_cam(self):
        self.cam.release()


if __name__ == '__main__':
    camera = Camera()
    try:
        while 1:
            camera.get_image(show=True)
    except Exception as e:
        print(f"exception->{e}")
    camera.cam.release()
    cv2.destroyAllWindows()