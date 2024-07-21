import { HttpClient } from '@angular/common/http';
import { Component, OnDestroy } from '@angular/core';
import { Subscription, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-gluten-detector',
  templateUrl: './gluten-detector.component.html',
  styleUrls: ['./gluten-detector.component.css']
})
export class GlutenDetectorComponent implements OnDestroy {
  selectedFile: File | null = null;
  taskId: string = '';
  result: string = '';
  private subscription: Subscription | undefined;

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  onUpload() {
    const formData = new FormData();
    formData.append('file', this.selectedFile!, this.selectedFile?.name || ''); 
    this.http.post<{ task_id: string }>('http://localhost:5000/upload', formData)
      .subscribe(response => {
        this.taskId = response.task_id;
        this.checkResult();
      });
  }

  checkResult() {
    if (this.taskId) {
      this.subscription = timer(0, 1000).pipe(
        switchMap(() => this.http.get<{ state: string, result?: string }>(`http://localhost:5000/result/${this.taskId}`))
      ).subscribe(response => {
        if (response.state === 'PENDING') {
          // Continuar comprobando cada segundo mientras el estado sea PENDING
        } else {
          this.result = response.result;
          this.subscription?.unsubscribe(); // Detener la suscripción una vez que se recibe el resultado
        }
      });
    }
  }

  ngOnDestroy() {
    // Asegurarse de desuscribirse para evitar memory leaks
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
