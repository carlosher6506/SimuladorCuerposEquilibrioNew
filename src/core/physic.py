import math

def calculate_tensions(weight, theta1, theta2):
    """Calculate tensions in the ropes."""
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)
    
    denominator = math.sin(theta1_rad + theta2_rad)
    if denominator == 0:
        return 0, 0
    
    T2 = weight * math.sin(theta1_rad) / denominator
    T1 = weight * math.sin(theta2_rad) / denominator
    
    return T1, T2

def solution(weight, theta1, theta2):
    """Alternative tension calculation method."""
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)
    T22 = weight / (math.sin(theta2_rad) + math.cos(theta2_rad) * math.tan(theta1_rad))
    T11 = weight / (math.sin(theta1_rad) + math.cos(theta1_rad) * math.tan(theta2_rad))
    
    return T11, T22

def calculate_body_position(anchor1_x, anchor2_x, anchor_y, T1, T2, theta1, theta2):
    """Calculate the position of the hanging body."""
    denominator = (T1 * math.cos(math.radians(theta1)) + T2 * math.cos(math.radians(theta2)))
    
    if denominator == 0:
        return anchor1_x, anchor_y
        
    body_x = (T2 * math.cos(math.radians(theta2)) * anchor1_x + T1 * math.cos(math.radians(theta1)) * anchor2_x) / denominator
    body_y = anchor_y + T1 * math.sin(math.radians(theta1))
    
    return int(body_x), int(body_y)

def conversor(kg):
    """Convert kilograms to Newtons."""
    return kg * 9.81