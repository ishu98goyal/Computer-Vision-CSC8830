I = imread("picture0.jpg");
imshow(I);

[x y] = ginput(2)



f = 1.636333e+03;
z0 = 713.74;
x0 = z0 * (x(1) / f)
x1 = z0 * (x(2)/ f)

y0 = z0 * (y(1) / f)
y1 = z0 * (y(2) / f)

distance = sqrt((x1-x0)^2 + (y1 - y0)^2)