%% May 9,2013, Movie Maker (MATLAB 2012B)
clc;
clear all;
% The global variables

scale=1;   % scale is for adjusting the data
ordermax=20;

% processing the first simulation data
load south.mat;
load middle.mat;
load north.mat;
load east.mat;
load west.mat;


fre001=value1(3:20004,1:136);
fre002=value2(3:20004,1:136);
fre003=value3(3:20004,1:136);
fre004=value4(3:20004,1:136);
fre005=value5(3:20004,1:136);

i=(138:2:408);
ang001=value1(3:20004,i);
ang002=value2(3:20004,i);
ang003=value3(3:20004,i);
ang004=value4(3:20004,i);
ang005=value5(3:20004,i);
 

for h=1:136
    ang01(:,h)= ang001(:,h)-ang001(:,112); 
    ang02(:,h)= ang002(:,h)-ang002(:,112); 
    ang03(:,h)= ang003(:,h)-ang003(:,112); 
    ang04(:,h)= ang004(:,h)-ang004(:,112); 
    ang05(:,h)= ang005(:,h)-ang005(:,112); 
end
ang01(:,1:135)=[ang01(:,1:111),ang01(:,113:136)];
ang02(:,1:135)=[ang02(:,1:111),ang02(:,113:136)];
ang03(:,1:135)=[ang03(:,1:111),ang03(:,113:136)];
ang04(:,1:135)=[ang04(:,1:111),ang04(:,113:136)];
ang05(:,1:135)=[ang05(:,1:111),ang05(:,113:136)];

fre01(:,1:135)=[fre001(:,1:111),fre001(:,113:136)];
fre02(:,1:135)=[fre002(:,1:111),fre002(:,113:136)];
fre03(:,1:135)=[fre003(:,1:111),fre003(:,113:136)];
fre04(:,1:135)=[fre004(:,1:111),fre004(:,113:136)];
fre05(:,1:135)=[fre005(:,1:111),fre005(:,113:136)];

for k=1:135

ang11(:,k)= detrend(ang01(:,k)); 
ang12(:,k)= detrend(ang02(:,k)); 
ang13(:,k)= detrend(ang03(:,k)); 
ang14(:,k)= detrend(ang04(:,k)); 
ang15(:,k)= detrend(ang05(:,k)); 
     
fre11(:,k)= detrend(fre01(:,k)); 
fre12(:,k)= detrend(fre02(:,k)); 
fre13(:,k)= detrend(fre03(:,k)); 
fre14(:,k)= detrend(fre04(:,k)); 
fre15(:,k)= detrend(fre05(:,k)); 
    
end

 [ra1,pa1]=corrcoef(ang11(:,:));
 [ra2,pa2]=corrcoef(ang12(:,:));
 [ra3,pa3]=corrcoef(ang13(:,:));
 [ra4,pa4]=corrcoef(ang14(:,:));
 [ra5,pa5]=corrcoef(ang15(:,:));
 
 [rf1,pf1]=corrcoef(fre11(:,:));
 [rf2,pf2]=corrcoef(fre12(:,:));
 [rf3,pf3]=corrcoef(fre13(:,:));
 [rf4,pf4]=corrcoef(fre14(:,:));
 [rf5,pf5]=corrcoef(fre15(:,:));
 

ya1=abs(ra1(41,:));
ya2=abs(ra2(41,:));
ya3=abs(ra3(41,:));
ya4=abs(ra4(41,:));
ya5=abs(ra5(41,:));

yf1=abs(rf1(41,:));
yf2=abs(rf2(41,:));
yf3=abs(rf3(41,:));
yf4=abs(rf4(41,:));
yf5=abs(rf5(41,:));

warning off MATLAB:griddata:DuplicateDataPoints
%% Load the Frequency correlation coefficients Info and data
%load EI_new_coffecients_Ivy.mat;

rf1=rf1(:,1:135);% Frequency correlation coefficients

load location.mat;
load MyColormaps;
%% Make the plot frame of EI 
figh = figure('position',[10 50 1280 800]);
set(figh,'Color','w');
ax1h  =axes('parent',figh,'position',[0.04 0.30 0.5 0.5]);
axis off;
ax2h = axes('parent',figh,'position',[0.50 0.30 0.5 0.5]);
axis off;
%% Make the display map frame of EI 
axes(ax2h);
maph = axesm('MapProjection','eqdcylin','MapParallels',[],'MapLatLimit',[24 51],'MapLonLimit',[-105 -60],...% Map Projection
    'MLineLocation',5,'MeridianLabel','on','MLabelLocation',15,'MLabelParallel','south',...
    'ParallelLabel','on','PLineLocation',10,'grid','on','frame','on');%,'Fontsize',14,'FontWeight','bold');
axis off;
% Define the color
EIcolor = [60,255,113]/255;
Ocolor = [211,211,211]/255;
seacolor = [176 224 230]/255;

NewBrunswick(EIcolor); 
NovaScotia(EIcolor);
PrinceEdwardIsland(Ocolor);
Quebec(Ocolor);
EastOcean(seacolor);
WECCTXME(Ocolor);

states = shaperead('usastatehi','UseGeoCoords',true,'BoundingBox',[[-100 -60]',[24 51]']);
geoshow(states);

unitlat=location(:,1);
unitlon=location(:,2);
%Preparing for the movie
perimlat = [24:.5:51,24:.5:51,24*ones(1,length(-105:.5:-60)),51*ones(1,length(-105:.5:-60))];
perimlon = [-105*ones(1,length(24:.5:51)),-60*ones(1,length(24:.5:51)),-105:.5:-60,-105:.5:-60];
plotm(unitlat',unitlon',400,'o','markerfacecolor','r','markeredgecolor','y','linewidth',1,'markersize',5);
latvec = [perimlat unitlat'];
lonvec = [perimlon unitlon'];
maplat = [24:.1:51];
maplon = [-105:.1:-60];
[latout,lonout] = meshgrat(maplat,maplon);
colormap(mycmap(1:57,:));
caxlim = [0 1];
caxis(maph,caxlim)
cbar_ax = colorbar('eastoutside','Fontsize',8,'FontWeight','bold');
hold(cbar_ax,'on');
aviobj = avifile('PSSE Frequency_Ivy','fps',0.5,'quality',100,'compression','None');

%% Make the movie
EventType='Generation Trip';
    for i=1:135
        try
         delete(b);
        end
        unitlati=unitlat(i,1);
        unitloni=unitlon(i,1);
        b=plotm(unitlati',unitloni',400,'*','markerfacecolor','k','markeredgecolor','k','linewidth',2,'markersize',15);
     try
         delete(a);
     end
        axes(ax1h);
        a=bar(rf2(i,1:135),0.2);  
        title('EI Simulation Frequency Correlation Coefficients Index','FontSize',15,'FontWeight','bold'); 
        xlabel('bus number');
        ylabel('correlation coefficients');
        ylim([0,1]);
    try
        delete(surfh)
    end
    axes(maph);
    title('             EI Simulation Frequency Correlation Coefficients Display ','FontSize',15,'FontWeight','bold');
    unitval = rf2(i,1:135);
    perimval = mean(unitval)*ones(1,length(perimlon));
    vecval = [perimval unitval];
    ZI = griddata(lonvec,latvec,vecval,lonout,latout,'cubic');
    surfh= surfm(latout,lonout,ZI);
    drawnow
    aviobj=addframe(aviobj,gcf);   
    pause(0.5);
    end
    aviobj=close(aviobj);
%delete(gcf)
clear FDRData frequencytrendmat unitlat unitlon unitval vecval aviobj fldnames f

 