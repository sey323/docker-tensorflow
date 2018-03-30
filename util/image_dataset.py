import sys , os
import random

import numpy as np
import cv2


# 画像をランダムの位置で切り抜くプログラム
def random_clip(img , clip_size , num = 1):
    clip_images = []
    height, width = img.shape[:2]

    # 画像をclip_sizeサイズごとにnum回切り抜く
    for y in range( num ):
        rand_y = random.randint(0,height - clip_size)
        rand_x = random.randint(0,width - clip_size)        
        clip_img = img[ rand_y : rand_y + clip_size, rand_x : rand_x + clip_size]
        clip_img = clip_img.flatten().astype(np.float32)/255.0
        clip_images.append(clip_img)

    return clip_images


# データセットから画像とラベルをランダムに取得
def random_sampling( images , labels , train_num , test_num = 0  ):
    image_train_batch = []
    label_train_batch = []

    #乱数を発生させ，リストを並び替える．
    random_seq = list(range(len(images)))
    random.shuffle(random_seq)

    # バッチサイズ分画像を選択
    image_train_batch = images[ :train_num ]
    label_train_batch = labels[ :train_num ]

    if test_num == 0: # 検証用データの指定がないとき
        return image_train_batch , label_train_batch
    else:
        image_test_batch = images[ train_num : train_num + test_num ]
        label_test_batch = labels[ train_num : train_num + test_num ]
        return image_train_batch , label_train_batch , image_test_batch , label_test_batch


# フォルダーの画像をランダム位置でクリップした後にリサイズして読み込む
def make( folder_name , img_size = 0 , clip_num = 0 , clip_size = 0 ,train_num = 0 , test_num = 0 ):
    train_image = []
    test_image = []
    train_label = []
    test_label= []

    # フォルダ内のディレクトリの読み込み
    classes = os.listdir( folder_name )

    for i, d in enumerate(classes):
        files = os.listdir( folder_name + '/' + d  )

        tmp_image = []
        tmp_label = []
        for f in files:
            # 1枚の画像に対する処理
            if not 'jpg' in f:# jpg以外のファイルは無視
                continue

            # 画像読み込み
            img = cv2.imread( folder_name+ '/' + d + '/' + f)
            # one_hot_vectorを作りラベルとして追加
            label = np.zeros(len(classes))
            label[i] = 1

            # リサイズをする処理
            if img_size != 0:
                img = cv2.resize( img , (img_size , img_size ))
                img = img.flatten().astype(np.float32)/255.0
                tmp_image.append(img)                
                tmp_label.append(label)
            elif clip_size != 0 and clip_num != 0:
                img = random_clip( img , clip_size , clip_num)
                tmp_image.extend( img )                    
                for j in range(clip_num):
                    tmp_label.append(label)
            else:
                img = img.flatten().astype(np.float32)/255.0
                tmp_image.append(img)
                tmp_label.append(label)


        # データセットのサイズが指定されているときはその枚数分ランダムに抽出する
        if train_num == 0 :
            train_image.extend( tmp_image )
            train_label.extend( tmp_label )
        #　テスト画像の指定がないとき
        elif test_num == 0 :
            sampled_image , sampled_label = random_sampling( tmp_image , tmp_label , train_num )
            train_image.extend( sampled_image )
            train_label.extend( sampled_label )
        else :
            sampled_train_image , sampled_train_label , sampled_test_image , sampled_test_label = random_sampling( tmp_image , tmp_label , train_num , test_num )
            train_image.extend( sampled_train_image )
            train_label.extend( sampled_train_label )
            test_image.extend( sampled_test_image )
            test_label.extend( sampled_test_label )

        print(d + 'read complete ,' + str(len(train_label)) + ' pictures exit')

    # numpy配列に変換
    train_image = np.asarray( train_image )
    train_label = np.asarray( train_label )

    if test_num != 0: #testデータセットがあるときは返り値が変わる
        test_image = np.asarray( test_image )
        test_label = np.asarray( test_label )
        return train_image , train_label , test_image , test_label

    return train_image , train_label
