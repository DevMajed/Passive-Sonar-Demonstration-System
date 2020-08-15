close all
clear
clc


IN2M = 0.0254;
% files = string({'right30deg1kHzFullSig.txt',  '1khz30degLeftFullSig.txt'});
files = string({'1khz30degRightFar.txt',  '1khz30degLeftFar.txt', '1khzCenterFar.txt'});

fileIn = files{3};

    %Read in data from .txt file provided
    formatSpec = '%f%f%f%f';
    fileID = fopen(fileIn, 'r');

    dataIn = textscan(fileID, formatSpec, 'delimiter', '\n', 'HeaderLines', 5, 'CollectOutput', true, 'TreatAsEmpty', '[-inf]');
    speakerData = cell2mat(dataIn);

    fclose(fileID);

    %Left and right amplitude data
    ampLeft = speakerData(:,2);
    ampRight = speakerData(:,4);
    
     %Dealing with NAN input
    for ii = 1:size(ampLeft)
        if isnan(ampLeft(ii))
            ampLeft(ii) = 0;
        end
    end
    for jj = 1:size(ampRight)
        if isnan(ampRight(jj))
            ampRight(jj) = 0;
        end
    end
    
    %Physical Values
    c = 340; %m/s
    d = 6*IN2M; %m
    fs = 48e3; %Hz
    ts = 1/fs;
    N = 10;
    maxTau = d/c;
    iStart = 1;
    sampWindow = floor(maxTau/ts);
    iStop = iStart + sampWindow-1;
    
    figure; 
    thetaMax = zeros(1,N);
    
    while (iStop < length(ampLeft))
        al = ampLeft(iStart:iStop);
        alhl = al;
        alhl(al >= 0) = 1;
        alhl(al < 0 ) = -1;
    
        
        ar = ampRight(iStart:iStop);
        arhl = ar;
        arhl(ar >= 0) = 1;
        arhl(ar < 0 ) = -1;
        
        L = length(al) + length(ar) - 1;
        
        theta = linspace(-90,90,L);
    %     tau = d*cosd(theta)/c;
    %     theta = acosd(c*tau/d);
        
        x = xcorr(arhl,alhl);
        s = linspace(-L/2,L/2,L);
    %     plot(theta,x);
        iMax = find(x == max(x));
        iMax = iMax(1);
        tauHat = s(iMax)*ts;
        tauHat_ms=tauHat/(1e-3);
        dist_inch = tauHat_ms*1e-3*340*39;
    %     iTheta = theta(iMax);
        thetaHat = theta(iMax);    
        thetaMax(1:N-1) = thetaMax(2:N);
        thetaMax(N) = thetaHat;
        thetaHat = mean(thetaMax)
        
        iStart = iStop+1;
        iStop = iStart + sampWindow-1;
    %     pause(0.5)
    end