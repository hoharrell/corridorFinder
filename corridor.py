import shapefile as shp # import package for shapefiles.



sf = shp.Reader("/Users/r_busch/Desktop/MR/finalproject/El Dorado.zip")

shapes = sf.shapes()

print(sf.shape(7).points)
