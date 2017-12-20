from PIL import Image
import struct
import os


def createFile(path):
	for i in xrange(10):
		os.mkdir(path + '\\' + str(i))


def read_image(idx_img, idx_label, path_img, path_label):
	list_file = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	fd_img = open(idx_img, 'rb')
	buf_img = fd_img.read()
	fd_img.close()
	fd_label = open(idx_label, 'rb')
	buf_label = fd_label.read()
	fd_label.close()
	wd_label = open(path_label, 'w+')

	createFile(path_img)

	index_img = 0
	index_label = 0

	magic, images, rows, cols = struct.unpack_from('>IIII', buf_img, index_img)
	index_img += struct.calcsize('>IIII')
	magic, label_num = struct.unpack_from('>II', buf_label, index_label)
	index_label += struct.calcsize('>II')

	for i in xrange(images):
		image = Image.new('L', (cols, rows))
		for x in xrange(rows):
			for y in xrange(cols):
				image.putpixel((y, x), int(struct.unpack_from('>B', buf_img, index_img)[0]))
				index_img += struct.calcsize('>B')
		label_item = int(struct.unpack_from('>B', buf_label, index_label)[0])
		index_label += struct.calcsize('>B')
		image.save(path_img + '\\' + str(label_item) + '\\' + str(label_item )+ '_' + str(list_file[label_item]) + '.png')
		wd_label.write(str(label_item) + '_' + str(list_file[label_item]) + "     " + str(label_item)+'\n')
		list_file[label_item] += 1
	wd_label.close()


def read_label(rlabelidx, wlabeltxt):
	fd = open(rlabelidx, 'rb')
	buf = fd.read()
	index = 0
	magic, label_num = struct.unpack_from('>II', buf, index)
	index += struct.calcsize('>II')
	wd = open(wlabeltxt, 'w+')
	fd.close()
	for i in xrange(label_num):
		label_item = int(struct.unpack_from('>B', buf, index)[0])
		index += 1
		wd.write(str(label_item) + '\n')
	wd.close()


if __name__ == '__main__':
	# read_image('C:\Users\Administrator\Desktop\caffe\Mnist-image\mytrain\\train-images.idx3-ubyte')
	read_image('C:\Users\Administrator\Desktop\caffe\Mnist-image\mytrain\\train-images.idx3-ubyte',
			   'C:\Users\Administrator\Desktop\caffe\Mnist-image\mytrain\\train-labels.idx1-ubyte',
			   'C:\Users\Administrator\Desktop\caffe\Mnist-image\mytrain\images',
			   'C:\Users\Administrator\Desktop\caffe\Mnist-image\mytrain\label\mytrain_label.txt')
