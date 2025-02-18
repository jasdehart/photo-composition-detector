from PIL import Image

import helper


# Function to draw rule of 1/3 on an input image
def draw_thirds_on_image(image_path, orient = "vertical", grid = 3):
    '''
    Draws the rule of 1/3 on an image.
    
    Args:
        image_path: string for image path
        orient: string indicating the direction to calculate the thirds
        grid: INT for drawing number of lines

    Returns:
        img: ImageObj original image pased in
        modified_img: An drawn image and point list from lines.
        tmp_point1+tmp_point2: joined LIST of points from lines
    '''
    
    # Load the input image
    img = Image.open(image_path)
    modified_img = img.copy()


    width, height = img.size
    if orient == 'vertical' and grid ==3:
        ''' If orientation is veritcal, draw lines vertical, which focuses on the width.'''

        start_point_x1, start_point_y1, end_point_x1, end_point_y1 = helper.vertical_line(width, side='left')
        start_point, end_point= helper.draw_line(modified_img, start_point_x1, start_point_y1, end_point_x1, end_point_y1)
        tmp_point1 = helper.points_on_line(start_point, end_point)


        ''' Drawing right third '''

        start_point_x2, start_point_y2, end_point_x2, end_point_y2 = helper.vertical_line(width, side='right')
        start_point, end_point = helper.draw_line(modified_img, start_point_x2, start_point_y2, end_point_x2, end_point_y2)
        tmp_point2 = helper.points_on_line(start_point, end_point)

        return img, modified_img, tmp_point1+tmp_point2
        
        
    elif orient == 'horizontal' and grid == 3:

        ''' If orientation is horizontal, draw lines horizontal, which focuses on the height.'''

        start_point_x1, start_point_y1, end_point_x1, end_point_y1 = helper.horizontal_line(height, width, side='top')
        start_point, end_point = helper.draw_line(modified_img, start_point_x1, start_point_y1, end_point_x1, end_point_y1)
        tmp_point1 = helper.points_on_line(start_point, end_point)


        ''' Drawing right third '''

        start_point_x2, start_point_y2, end_point_x2, end_point_y2 = helper.horizontal_line(height, width, side='bottom')
        start_point, end_point = helper.draw_line(modified_img, start_point_x2, start_point_y2, end_point_x2, end_point_y2)
        tmp_point2 = helper.points_on_line(start_point, end_point)

        return img, modified_img, tmp_point1+tmp_point2

    elif orient =="blocks" and grid ==9:

        ''' Draw lines vertical, which focuses on the width.'''
        start_point_x1, start_point_y1, end_point_x1, end_point_y1 = helper.vertical_line(width, side='left')
        start_point, end_point = helper.draw_line(modified_img, start_point_x1, start_point_y1, end_point_x1, end_point_y1)
        tmp_point1 = helper.points_on_line(start_point, end_point)


        ''' Drawing right third '''

        start_point_x2, start_point_y2, end_point_x2, end_point_y2 = helper.vertical_line(width, side='right')
        start_point, end_point = helper.draw_line(modified_img, start_point_x2, start_point_y2, end_point_x2, end_point_y2)
        tmp_point2 = helper.points_on_line(start_point, end_point)


        ''' Draw lines horizontal, which focuses on the height.'''

        start_point_x1, start_point_y1, end_point_x1, end_point_y1 = helper.horizontal_line(height, width, side='top')
        start_point, end_point = helper.draw_line(modified_img, start_point_x1, start_point_y1, end_point_x1, end_point_y1)
        tmp_point3 = helper.points_on_line(start_point, end_point)


        ''' Drawing right third '''

        start_point_x2, start_point_y2, end_point_x2, end_point_y2 = helper.horizontal_line(height, width, side='bottom')
        start_point, end_point = helper.draw_line(modified_img, start_point_x2, start_point_y2, end_point_x2, end_point_y2)
        tmp_point4 = helper.points_on_line(start_point, end_point)

        return img, modified_img, tmp_point1+tmp_point2+tmp_point3+tmp_point4