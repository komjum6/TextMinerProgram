from flask import Flask, render_template, request, flash, redirect, get_flashed_messages
from wtforms import Form, BooleanField, TextAreaField, PasswordField, validators
from flask_wtf import FlaskForm
import os
import re
import time

aminoAcidMap = {                #Een aminozuurdictionary
                'TTT' : 'F',
                'TTC' : 'F',
                'TTA' : 'L',
                'TTG' : 'L',
                
                'TCT' : 'S',
                'TCC' : 'S',
                'TCA' : 'S',
                'TCG' : 'S',

                'TAT' : 'Y',
                'TAC' : 'Y',
                'TAA' : '*',
                'TAG' : '*',

                'TGT' : 'C',
                'TGC' : 'C',
                'TGA' : '*',
                'TGG' : 'W',


                'CTT' : 'L',
                'CTC' : 'L',
                'CTA' : 'L',
                'CTG' : 'L',

                'CCT' : 'P',
                'CCC' : 'P',
                'CCA' : 'P',
                'CCG' : 'P',

                'CAT' : 'H',
                'CAC' : 'H',
                'CAA' : 'Q',
                'CAG' : 'Q',

                'CGT' : 'R',
                'CGC' : 'R',
                'CGA' : 'R',
                'CGG' : 'R',


                'ATT' : 'I',
                'ATC' : 'I',
                'ATA' : 'I',
                'ATG' : 'M',

                'ACT' : 'T',
                'ACC' : 'T',
                'ACA' : 'T',
                'ACG' : 'T',

                'AAT' : 'N',
                'AAC' : 'N',
                'AAA' : 'K',
                'AAG' : 'K',

                'AGT' : 'S',
                'AGC' : 'S',
                'AGA' : 'R',
                'AGG' : 'R',


                'GTT' : 'V',
                'GTC' : 'V',
                'GTA' : 'V',
                'GTG' : 'V',

                'GCT' : 'A',
                'GCC' : 'A',
                'GCA' : 'A',
                'GCG' : 'A',

                'GAT' : 'D',
                'GAC' : 'D',
                'GAA' : 'E',
                'GAG' : 'E',

                'GGT' : 'G',
                'GGC' : 'G',
                'GGA' : 'G',
                'GGG' : 'G'}

class DNAtoProtein(FlaskForm):
    DNAseq = TextAreaField('DNAsequence', [validators.Length(min=1, max=400)])

def DNAconversion():
    form = DNAtoProtein()
    #print(form.errors)
    if request.method == 'POST':
        if request.form['action'] == 'DNA to Protein':
            raw_dna = request.form['dna']
            raw_dna = raw_dna.upper()
            pattern = re.compile(r"[^ATGC]")
            if bool(re.match(pattern, raw_dna)) == True:
                flash("Nope, not a good sequence")
            else:
                flash("Succes")
                skew = 0 
                if len(raw_dna) % 3 == 1: 
                    skew = 1
                if len(raw_dna) % 3 == 2:
                    skew = 2
                try:
                    form.raw_dna = "".join([aminoAcidMap[raw_dna[x:x+3]] for x in range(0, (len(raw_dna)-skew), 3)])
                except:
                    pass
                    
        if request.form['action'] == 'DNA to RNA':
            raw_dna = request.form['dna']
            raw_dna = raw_dna.upper()
            pattern = re.compile(r"[^ATGC]")
            if bool(re.match(pattern, raw_dna)) == True:
                flash("Nope, not a good sequence")
            else:
                flash("Succes")
                form.raw_dna = raw_dna.replace('T','U')
            
    #last_flashed_message()
    
    return form

def last_flashed_message():
        """Return last flashed message by flask."""
        messages = get_flashed_messages()
        if len(messages) > 0:
            return messages[-1]
        else:
            return None 

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if request.form['action'] == 'Submit Bestand':
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(request.url)