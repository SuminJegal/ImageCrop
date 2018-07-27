import os

for dirname, dirnames, filenames in os.walk('N:\\04-Team\\Character\\Project\\SummerPrj2018\\deepnaht\\images\\2018-07-05.synced'):

    # create dir
    for subdirname in dirnames:
        name = os.path.join(dirname, subdirname)
        print('dir : ', name)
        my_path = os.path.join('N:\\04-Team\\Character\\Project\\SummerPrj2018\\deepnaht\\images\\crop_512', subdirname)
        try:
            if not (os.path.isdir(my_path)):
                os.makedirs(os.path.join(my_path))
                print('create success in ', my_path)
        except OSError as e:
            print("Failed to create directory!!!!!")
            raise

    # count = 0
    # for filename in filenames:
    #     if count %1000 ==0:
    #         print(dirname.split('\\')[8])
    #         print(os.path.join(dirname, filename))
    #     count += 1
