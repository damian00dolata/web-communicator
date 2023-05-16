import type IObserver from "./IObserver";

export default interface IObservable {
   attach(observer: IObserver): void;
   detach(observer: IObserver): void;
   notify(): void;
}