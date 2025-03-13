// Copyright 2025 Google LLC. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
import { Injectable } from '@angular/core';
import { HttpClient, HttpDownloadProgressEvent, HttpEvent, HttpEventType, HttpHeaders } from '@angular/common/http';
import { Observable, Subject, tap } from 'rxjs';
import { CreateChatRequest } from '../models/chat.model';
import { environment } from 'src/environments/environment';
import { SessionService } from './user/session.service';

// include "/" or ":" in the environment.ts file
const chatsUrl = `${environment.backendURL}streamQuery`;


@Injectable({
  providedIn: 'root'
})
export class ChatService {

  constructor(private http: HttpClient, private sessionService: SessionService) {}

  postChat(query: string): Observable<HttpEvent<string>> {
    if (!this.sessionService.getSession()) {
      this.sessionService.createSession();
    }
    // const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

    const headers = new HttpHeaders({
      'Authorization': 'Bearer ya29.A0AeXRPp6npc-9VEvu35RIldWwBnBGo4O01paofsm-vK9clNSM0PaFCtiXUoQD2PtAZEydmjQTm0wAD8-tuTcgmQrJx2ov60QaEVTkApxBYIiI28KDiTCilNMjNSAT3jpwXJwJgXpjoDRWB6KVchoisoFyj3E3NWShQIxAdXmvYQEMgiY2W7uJJbsP9dgIiCq8SJJps0CgvEGKMgaCgYKAcASARMSFQHGX2MiKKEFeq_xdhuq-3hc4QHhoA0213',
      'Content-Type': 'application/json' });

    query = query.replace(/\s+/g, " ").trim();
    const body: CreateChatRequest = {
      input: {
        input: {
          messages: [
            {
              content: query,
              type: "human",
            }
          ],
          session_id: this.sessionService.getSession()!,
        }
      }
    };

    return this.http
      .post(chatsUrl, body, {
        headers,
        observe: "events",
        responseType: "text",
        reportProgress: true,
      })
  }
}
