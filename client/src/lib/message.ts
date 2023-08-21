class Message {
  clientName: string;
  message: string;
  date: string;
 
  constructor(clientName: string, message: string, date: string) {
    this.clientName = clientName;
    this.message = message;
    this.date = date;
  }
}
 
export { Message }