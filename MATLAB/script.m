% load handel.mat

% read double value and write to wav file
 Fs = 8192; % sample rate
 filename = 'musicwithfan_mono_afterkalman.wav';
% audiowrite(<filename>,<sampledatavector>,<sampleratevalue>)
 audiowrite(filename,handle,Fs); 


% read wav file and output to sample data to "handel" and sample
% rate to "Fs"
 [handel,Fs] = audioread('handel.wav');
 
% play the sound with "double" values
 sound(handle,Fs);
