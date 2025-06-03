import { Component, Host, HostListener, inject, OnInit } from '@angular/core';
import { MaterialModule } from '../../../shared/material-module/material-module';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-upload-data',
  imports: [MaterialModule,FormsModule,ReactiveFormsModule,CommonModule],
  templateUrl: './upload-data.html',
  styleUrl: './upload-data.scss'
})
export class UploadData implements OnInit {
  uploadForm!:FormGroup;
  selectedFileName: string = '';
  private _snackBar = inject(MatSnackBar);
  constructor(private fb:FormBuilder){}
  ngOnInit(): void {
    this.uploadForm = this.fb.group({
      file: [null,Validators.required],
      selectedDate:['', Validators.required],
    });
  }
  @HostListener('drop',['$event'])
  public fileDroppedEvent(event:any) {
    console.log('file droppedEvent', event.dataTransfer);
    console.log('file droppedEvent', event.target);
    this.preventDefaultAndStopPropagation(event);
    let filesObj = event.target.files || event.dataTransfer.files;
    this.selectedFiles(filesObj);
  }
  clearSelection(val:any) {
    if (val.files && val.files.length > 0) {
      val.value = '';
    }
  }
  @HostListener('dragover', ['$event'])
  @HostListener('dragenter', ['$event'])
  @HostListener('dragleave', ['$event'])
  @HostListener('dragend', ['$event'])
  @HostListener('drag', ['$event'])
  @HostListener('dragstart', ['$event'])
  public preventDefaultAndStopPropagation(event:any) {
    event.preventDefault();
    event.stopPropagation();
  }

  selectedFiles(filesObj:any) {
    const selectedFile = filesObj[0];
    this.uploadForm.patchValue({file:selectedFile});
    this.uploadForm.get('file')?.updateValueAndValidity();
    this.selectedFileName = selectedFile.name;
    console.log('Selected File:', selectedFile);
  }


  uploadFile() {
    console.log('Form Value:', this.uploadForm.value);
    let xhr = new XMLHttpRequest();
    let self=this;
    xhr.open('POST', 'http://localhost:8000/upload-excel', true);
    xhr.withCredentials = true;
    xhr.setRequestHeader('Authorization', 'Bearer ' + sessionStorage.getItem('access_token'));
    const sendable = new FormData();
    sendable.append('file', this.uploadForm.value.file);
    sendable.append('date', this.uploadForm.value.selectedDate);
    xhr.send(sendable);
    xhr.onreadystatechange = function() {
      if(xhr.readyState === XMLHttpRequest.DONE) {
        if(xhr.status === 200) {
          self._snackBar.open(JSON.parse(xhr.responseText).message, 'Close', {
            duration: 3000,
          });
          self.uploadForm.reset();
          self.selectedFileName = '';
        } else {
          console.error('Error uploading file:', xhr.status, xhr.statusText);
        }
      }
    }
  }
}
