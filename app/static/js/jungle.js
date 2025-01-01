// Based on https://github.com/cwilso/Audio-Input-Effects/blob/master/js/jungle.js

// Copyright 2012, Google Inc.
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
// 
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

function createFadeBuffer(context, activeTime, fadeTime) {
    var length1 = activeTime * context.sampleRate;
    var length2 = (activeTime - 2*fadeTime) * context.sampleRate;
    var length = length1 + length2;
    var buffer = context.createBuffer(1, length, context.sampleRate);
    var p = buffer.getChannelData(0);
        
    var fadeLength = fadeTime * context.sampleRate;

    var fadeIndex1 = fadeLength;
    var fadeIndex2 = length1 - fadeLength;
    
    // 1st part - fade in
    for (var i = 0; i < fadeLength; ++i) {
        var value = Math.sin((i / fadeLength) * Math.PI / 2);
        p[i] = value;
    }

    // Middle - constant
    for (var i = fadeIndex1; i < fadeIndex2; ++i) {
        p[i] = 1;
    }
    
    // 2nd part - fade out
    for (var i = fadeIndex2; i < length1; ++i) {
        var value = Math.sin(((length1 - i) / fadeLength) * Math.PI / 2);
        p[i] = value;
    }

    return buffer;
}

function createDelayTimeBuffer(context, activeTime, fadeTime, shiftUp) {
    var length1 = activeTime * context.sampleRate;
    var length2 = (activeTime - 2*fadeTime) * context.sampleRate;
    var length = length1 + length2;
    var buffer = context.createBuffer(1, length, context.sampleRate);
    var p = buffer.getChannelData(0);

    // 1st part - fade in
    for (var i = 0; i < length1; ++i) {
        if (shiftUp)
            p[i] = (length1-i)/length;
        else
            p[i] = i / length1;
    }

    return buffer;
}

var delayTime = 0.100;
var fadeTime = 0.050;
var bufferTime = 0.100;

function Jungle(context) {
    this.context = context;
    
    // Create nodes for the input and output of this "module".
    var input = context.createGain();
    var output = context.createGain();
    this.input = input;
    this.output = output;
    
    // Pre-processing: add a small amount of gain to reduce artifacts
    var inputGain = context.createGain();
    inputGain.gain.value = 0.95;
    input.connect(inputGain);

    // Delay modulation.
    var mod1 = context.createBufferSource();
    var mod2 = context.createBufferSource();
    var mod3 = context.createBufferSource();
    var mod4 = context.createBufferSource();
    this.shiftDownBuffer = createDelayTimeBuffer(context, bufferTime, fadeTime, false);
    this.shiftUpBuffer = createDelayTimeBuffer(context, bufferTime, fadeTime, true);
    mod1.buffer = this.shiftDownBuffer;
    mod2.buffer = this.shiftDownBuffer;
    mod3.buffer = this.shiftUpBuffer;
    mod4.buffer = this.shiftUpBuffer;
    mod1.loop = true;
    mod2.loop = true;
    mod3.loop = true;
    mod4.loop = true;

    // for switching between oct-up and oct-down
    var mod1Gain = context.createGain();
    var mod2Gain = context.createGain();
    var mod3Gain = context.createGain();
    mod3Gain.gain.value = 0;
    var mod4Gain = context.createGain();
    mod4Gain.gain.value = 0;

    mod1.connect(mod1Gain);
    mod2.connect(mod2Gain);
    mod3.connect(mod3Gain);
    mod4.connect(mod4Gain);

    // Delay lines
    var delay1 = context.createDelay();
    var delay2 = context.createDelay();
    delay1.delayTime.value = delayTime;
    delay2.delayTime.value = delayTime;
    mod1Gain.connect(delay1.delayTime);
    mod2Gain.connect(delay2.delayTime);
    mod3Gain.connect(delay1.delayTime);
    mod4Gain.connect(delay2.delayTime);

    // Crossfading
    var fade1 = context.createBufferSource();
    var fade2 = context.createBufferSource();
    var fadeBuffer = createFadeBuffer(context, bufferTime, fadeTime);
    fade1.buffer = fadeBuffer
    fade2.buffer = fadeBuffer;
    fade1.loop = true;
    fade2.loop = true;

    var mix1 = context.createGain();
    var mix2 = context.createGain();
    mix1.gain.value = 0;
    mix2.gain.value = 0;

    fade1.connect(mix1.gain);    
    fade2.connect(mix2.gain);
        
    // Connect processing graph.
    inputGain.connect(delay1);
    inputGain.connect(delay2);    
    delay1.connect(mix1);
    delay2.connect(mix2);
    mix1.connect(output);
    mix2.connect(output);
    
    // Add a clean signal path
    var clean = context.createGain();
    clean.gain.value = 0;
    inputGain.connect(clean);
    clean.connect(output);
    this.clean = clean;
    
    // Start
    var t = context.currentTime + 0.050;
    var t2 = t + bufferTime - fadeTime;
    mod1.start(t);
    mod2.start(t2);
    mod3.start(t);
    mod4.start(t2);
    fade1.start(t);
    fade2.start(t2);

    this.mod1 = mod1;
    this.mod2 = mod2;
    this.mod1Gain = mod1Gain;
    this.mod2Gain = mod2Gain;
    this.mod3Gain = mod3Gain;
    this.mod4Gain = mod4Gain;
    this.mod3 = mod3;
    this.mod4 = mod4;
    this.fade1 = fade1;
    this.fade2 = fade2;
    this.mix1 = mix1;
    this.mix2 = mix2;
    this.delay1 = delay1;
    this.delay2 = delay2;
    
    this.setDelay(delayTime);
}

Jungle.prototype.setDelay = function(delayTime) {
    this.delay1.delayTime.setTargetAtTime(delayTime, 0, 0.010);
    this.delay2.delayTime.setTargetAtTime(delayTime, 0, 0.010);
}

Jungle.prototype.setPitchOffset = function(semitones) {
    if (semitones === 0) {
        // When no pitch shift, use the clean signal
        this.clean.gain.value = 1;
        this.mix1.gain.value = 0;
        this.mix2.gain.value = 0;
    } else {
        // Use pitch shifted signal
        this.clean.gain.value = 0;
        this.mix1.gain.value = 1;
        this.mix2.gain.value = 1;
        
        var factor = Math.pow(2.0, semitones / 12.0);
        this.setDelay(delayTime * factor);
        
        // Adjust gains for up/down shift
        if (semitones > 0) {
            this.mod1Gain.gain.value = 0;
            this.mod2Gain.gain.value = 0;
            this.mod3Gain.gain.value = 1;
            this.mod4Gain.gain.value = 1;
        } else {
            this.mod1Gain.gain.value = 1;
            this.mod2Gain.gain.value = 1;
            this.mod3Gain.gain.value = 0;
            this.mod4Gain.gain.value = 0;
        }
    }
}

window.Jungle = Jungle; 