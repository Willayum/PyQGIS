%% Extracting building polygons and census data within city boundary

clc
close all
clear all
     

%% City boundary, buildings, Census input data
lv = load('citybd_temp.mat'); citybd = lv.citybd; % census city boundary (named city/place)

s_build = shaperead('./Virginia/Virginia_buildings/Virginia.shp'); % building polygon shapefile, (state based)

s_block = shaperead('./Virginia/tabblock2010_51_pophu/tabblock2010_51_pophu.shp'); % census blocks

%% Building extraction
no_cpu = 40;
if ~isempty(gcp('nocreate'))
    delete(gcp);
    parpool(no_cpu);
else
    parpool(no_cpu);
end
parfor i = 1: length(s_build)
    bbc(i,:) = mean(s_build(i).BoundingBox,1);
end
delete(gcp)

building_in = inpolygon(bbc(:,1), bbc(:,2), citybd(:,1), citybd(:,2));

s_build = s_build(building_in);


%% Census block extraction
for i = 1: length(s_block)
    xbd = s_block(i).X(1:end-1); ybd = s_block(i).Y(1:end-1);
    block_center(i,:) = [mean(xbd) mean(ybd)];
end

block_in = inpolygon(block_center(:,1), block_center(:,2), citybd(:,1), citybd(:,2));
s_block = s_block(block_in);

%% Delete city boundry temp file
delete citybd_temp.mat

%% Save city named file (city boundry, city buildings, and city census blocks)
save Richmond_virginia citybd s_build s_block