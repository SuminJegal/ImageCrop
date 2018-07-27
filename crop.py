import cv2
import os
face_cascade = cv2.CascadeClassifier('C:\\Users\\sumin\\Anaconda3\\envs\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml')
alt_face_cascade = cv2.CascadeClassifier('C:\\Users\\sumin\\Anaconda3\\envs\\Lib\\site-packages\\cv2\\data\\haarcascade_profileface.xml')
done_list = list()
# done_list = ['01-center', '01-center_upper', '01-left_01', '01-left_02', '01-left_03', '01-right_01', '01-right_02', '01-right_03',
#              '02-center', '02-center_upper', '02-left_01', '02-left_02', '02-left_03', '02-right_01', '02-right_02', '02-right_03',
#              '03-center', '03-center_upper', '03-left_01', '03-left_02', '03-left_03', '03-right_01', '03-right_02', '03-right_03',
#              '04-center', '04-center_upper', '04-left_01', '04-left_02', '04-left_03', '04-right_01', '04-right_02', '04-right_03',
#              '08-center', '08-center_upper', '08-left_01', '08-left_02', '08-left_03', '08-right_01', '08-right_02', '08-right_03',
#              '09-center', '09-center_upper', '09-left_01', '09-left_02', '09-left_03', '09-right_01', '09-right_02', '09-right_03',
#              '10-center', '10-center_upper', '10-left_01', '10-left_02', '10-left_03', '10-right_01', '10-right_02', '10-right_03',
#              '11-center', '11-center_upper', '11-left_01', '11-left_02', '11-left_03', '11-right_01', '11-right_02', '11-right_03',
#              '12-center', '12-center_upper', '12-left_01', '12-left_02', '12-left_03', '12-right_01', '12-right_02', '12-right_03',
#              '13-center', '13-center_upper', '13-left_01', '13-left_02', '13-left_03', '13-right_01', '13-right_02', '13-right_03',
#              '14-center', '14-center_upper', '14-left_01', '14-left_02', '14-left_03', '14-right_01', '14-right_02', '14-right_03']


def get_image(img_source):
    return cv2.imread(img_source)

def get_face_boundary(img, path):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_flip = cv2.flip(img, 1)
    gray_flip = cv2.cvtColor(img_flip, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(300, 300))
    alt_faces = alt_face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(300, 300))
    faces_flip = face_cascade.detectMultiScale(gray_flip, 1.3, 5, minSize=(300,300))
    alt_faces_flip = alt_face_cascade.detectMultiScale(gray_flip, 1.3, 5, minSize=(300, 300))
    if len(faces) != 0:
        return faces, True
    elif len(alt_faces) != 0:

        return alt_faces, True
    elif len(faces_flip) != 0:
        return faces_flip, False
    elif len(alt_faces_flip) != 0:
        return alt_faces_flip, False
    else :
        print("Fail to find face boundary!!!! in ", path)
        return faces, True

def save_img(img, boundary, dirname, filename, tag):
    x, y, w, h = boundary[0][0], boundary[0][1], boundary[0][2], boundary[0][3]
    w_em = (int)(w*0.2)
    h_em = (int)(h*0.2)
    if (y-h_em) < 0:
        w_em = (int)(w*0.1)
        h_em = (int)(h*0.1)
    x = x-w_em
    y = y-h_em
    w = w+w_em+w_em
    h = h+h_em+h_em
    if tag is True:
        img_trim = img[y:y+h, x:x+w]
    else :
        img_flip = cv2.flip(img, 1)
        img_trim = img_flip[y:y + h, x:x + w]
        img_trim = cv2.flip(img_trim, 1)
    want_w = 512
    want_h = 512
    dim = (want_w, want_h)
    img_trim = cv2.resize(img_trim, dim, interpolation=cv2.INTER_AREA)
    save_dir = os.path.join('N:\\04-Team\\Character\\Project\\SummerPrj2018\\deepnaht\\images\\crop_512',  dirname.split('\\')[8])
    save_dir = os.path.join(save_dir, 'cr_' + filename )
    cv2.imwrite(save_dir, img_trim)

def visit_subfolder_crop_image(source, done_list):
    for dirname, dirnames, filenames in os.walk(source):
        print(done_list)
        count = 0
        if len(dirname.split('\\')) < 9 :
            continue
        elif dirname.split('\\')[8] in done_list:
            continue
        for filename in filenames:
            if filename[-3:] != 'jpg':
                continue
            current_file = os.path.join(dirname, filename)
            if count % 500 == 0:
                print("Now in ", current_file, " ...")
            img = cv2.imread(current_file)
            faces, tag = get_face_boundary(img, current_file)
            if len(faces) < 1:
                try:
                    save_img(img, before_faces, dirname, filename, tag)
                except:
                    print("Excepion occured!!!!! in {}\\{}", dirname, filename)
                    pass
            else :
                save_img(img, faces, dirname, filename, tag)
                before_faces = faces
            count += 1
        done_list.append(dirname.split('\\')[8])

def main():
    visit_subfolder_crop_image('N:\\04-Team\\Character\\Project\\SummerPrj2018\\deepnaht\\images\\2018-07-05.synced', done_list)

if __name__ == '__main__':
    main()
