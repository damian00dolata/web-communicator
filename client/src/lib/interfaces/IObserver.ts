import type IObservable from "./IObservable";

export default interface IObserver {
  update(observable: IObservable): void;
}