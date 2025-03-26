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

const env: string = 'dev';

let backendURL: string;
let chatbotName: string;

switch (env) {
  case 'prod':
    backendURL = "https://your-production-backend.com/"; // Replace with your production URL
    chatbotName = "your-production-chatbot-name"; // Replace with your production chatbot name
    break;
  case 'stage':
    backendURL = "https://your-staging-backend.com/"; // Replace with your staging URL
    chatbotName = "your-staging-chatbot-name"; // Replace with your staging chatbot name
    break;
  case 'dev':
  default:
    backendURL = "http://localhost:8000/";
    chatbotName = "agentsmithy-starter-agent";
    break;
}

export const environment = {
  production: env === 'prod',
  backendURL: backendURL,
  chatbotName: chatbotName,
  environmentName: env, 
};
