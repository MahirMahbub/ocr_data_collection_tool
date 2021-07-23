def img_similarity(img1_path,img2_path):
    import cv2
    try:
        img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)

        good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
        print(len(good))
        print(len(matches))
        similarity = len(good) / len(matches)
        # print("The similarity of the two pictures is: %s"% similarity)
        return similarity

    except Exception as e:
        print(e)
        # print('Unable to calculate the similarity of two pictures')
        return False