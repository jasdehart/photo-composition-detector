#! /usr/bin python3.12
 
import modeler
import helper
import thirds

# add logging and argparse, if main statement
import argparse
import logging
import sys

def main(image_path, orient, grid):

    processor, model = modeler.loadModel()
    logging.info('Model loaded!')

    data, img, img_point_list = thirds.draw_thirds_on_image(image_path, orient=orient, grid=grid)
    logging.info('Finding Rule of Thirds...')
    
    inputVals = modeler.encodeImage(processor, data)
    logging.info('Encoding image for features.')

    output = modeler.runModel(model, inputVals)
    logging.info('Running model on feature vectors.')

    preds = modeler.predictClass(data, processor, output)
    logging.info('Predicting object(s) in image')

    helper.computeItem(model, preds)

    box_width, box_height, box_coords = helper.boundedImage(img, model, preds)
    logging.info('Bounding box information!')

    closest_point, numberp, min_distance = helper.closest_point_and_distance(box_coords, img_point_list)
    logging.info(f'Found the closest center point: {closest_point}, point number: {numberp}, and Dist away: {min_distance}')


if __name__=="__main__":

    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--image", help="image path for detection", type=str, required=True)
    parser.add_argument("-o","--orient", help="orientation for thirds", type=str, choices=["vertical", "horizontal", "blocks"], default='vertical')
    parser.add_argument("-g","--grid", help="grid size", type=int, choices=[3,9], default=3)

    logging.info('Setting up variables')

    args = parser.parse_args()
    
    image_path = args.image

    if args.orient == 'blocks' and args.grid != 9:
        logging.warning("Blocks orientation requires 9 as grid size")
        sys.exit(1)
    elif args.orient == 'vertical' and args.grid != 3:
        logging.warning("Vertical and Horizontal orientation requires 3 as grid size")
        sys.exit(1)
    elif args.orient == 'horizontal' and args.grid != 3:
        logging.warning("Vertical and Horizontal orientation requires 3 as grid size")
        sys.exit(1)



    main(image_path, args.orient, args.grid)