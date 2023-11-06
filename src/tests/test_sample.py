import pytest
from OpenGLEarth import OpenGLEarth


@pytest.fixture(scope="module")
def app():
    app = OpenGLEarth()
    yield app


def test_rotate(app):
    old_rotation_angle_x = app.rotation_angle_x
    old_rotation_angle_y = app.rotation_angle_y
    app.rotate()
    new_rotation_angle_x = app.rotation_angle_x
    new_rotation_angle_y = app.rotation_angle_y
    assert old_rotation_angle_x != new_rotation_angle_x and old_rotation_angle_y != new_rotation_angle_y
