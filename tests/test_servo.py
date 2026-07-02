from servo_motion import calculate_angle

def test_motion():
    assert calculate_angle(1) == 180

def test_no_motion():
    assert calculate_angle(0) == 0