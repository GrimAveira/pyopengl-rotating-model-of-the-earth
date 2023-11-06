import sys
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PIL import Image


class OpenGLEarth():
    """Class OpenGLEarth used to create a OpenGL application

    Shows the rotating sphere with texture of the earth

    """

    def __init__(self, window_width=800, window_height=600, texture_path="../img/earth_texture.jpg"):

        self.window_width = window_width
        self.window_height = window_height
        self.texture_path = texture_path

        # start value rotation angle for sphere
        self.rotation_angle_x = 0.0
        self.rotation_angle_y = 0.0

    def __load_texture(self):
        """Loads the texture of the earth from a file 

        and converts it to the desired data format for OpenGL

        """
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # conversion
        image = Image.open(self.texture_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image_data = image.convert("RGBA").tobytes()

        # applying a texture to an object
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width,
                     image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)

        return texture_id

    def __init(self):
        """Initializes OpenGL, turns on lighting, turns on texturing, 

        loads the ground texture and sets the position of the light source

        """

        # turning on the light source
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        # configurating light source
        light_position = [1.0, 1.0, 1.0, 0.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_TEXTURE_2D)
        texture_id = self.__load_texture()
        glBindTexture(GL_TEXTURE_2D, texture_id)

    def __close(self, key):
        """Close app after press Escape
        """

        if key == b'\x1b':
            sys.exit(0)

    def __draw_sphere(self):
        """Draws a sphere using OpenGL.

        Uses triangulation to create the surface of a sphere.

        """

        radius = 0.5
        num_slices = 50
        num_stacks = 50

        # the latitude values (lat 0 and lat 1) for the current stack are calculated.
        for i in range(num_stacks):
            lat0 = math.pi * (-0.5 + float(i) / num_stacks)
            lat1 = math.pi * (-0.5 + float(i + 1) / num_stacks)
            sin_lat0 = math.sin(lat0)
            cos_lat0 = math.cos(lat0)
            sin_lat1 = math.sin(lat1)
            cos_lat1 = math.cos(lat1)

            glBegin(GL_TRIANGLE_STRIP)
            for j in range(num_slices + 1):
                lng = 2.0 * math.pi * float(j) / num_slices
                sin_lng = math.sin(lng)
                cos_lng = math.cos(lng)

                x0 = cos_lng * cos_lat0
                y0 = sin_lng * cos_lat0
                z0 = sin_lat0

                x1 = cos_lng * cos_lat1
                y1 = sin_lng * cos_lat1
                z1 = sin_lat1

                glNormal3f(x0, y0, z0)
                glTexCoord2f(float(j) / num_slices, float(i) / num_stacks)
                glVertex3f(radius * x0, radius * y0, radius * z0)

                glNormal3f(x1, y1, z1)
                glTexCoord2f(float(j) / num_slices, float(i + 1) / num_stacks)
                glVertex3f(radius * x1, radius * y1, radius * z1)
            glEnd()

    def __display(self):
        """Clears buffers, sets projection and modeling matrices, rotates the sphere

        and calls the __draw_sphere method to draw the sphere.

        """

        # clearing buffers and adapting to window sizes
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = float(self.window_width) / float(self.window_height)
        gluPerspective(45.0, aspect_ratio, 0.1, 100.0)

        # setting the camera position
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glRotatef(self.rotation_angle_x, 1.0, 0.0, 0.0)
        glRotatef(self.rotation_angle_y, 0.0, 1.0, 0.0)

        self.__draw_sphere()

        glutSwapBuffers()

    def __reshape(self, width, height):
        """It installs a new OpenGL viewport when resizing the window
        """

        glViewport(0, 0, width, height)

    def rotate(self):
        """Increase rotation angle sphere
        """

        self.rotation_angle_x += 0.5
        self.rotation_angle_y += 0.5

    def __idle(self):
        """Called in standby mode for rerender

        sphere after rotate 

        """

        self.rotate()
        glutPostRedisplay()

    def run(self):
        """Initializes GLUT, creates an application window, sets

        callback functions (display, reshape, keyboard, idle)

        and starts the main GLUT loop for event processing

        """

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.window_width, self.window_height)
        glutCreateWindow(b"OpenGL Earth")
        self.__init()
        glutDisplayFunc(self.__display)
        glutReshapeFunc(self.__reshape)
        glutKeyboardFunc(self.__close)
        glutIdleFunc(self.__idle)
        glutMainLoop()
