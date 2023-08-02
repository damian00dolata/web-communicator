class Message {
   clientName: string;
   message: string;
 
   constructor(clientName: string, message: string) {
     this.clientName = clientName;
     this.message = message;
   }
 }
 
 export { Message }