import { fetchAll } from "./api/client";
import { Headroom } from "../meter";

export function render(): string {
  return `${fetchAll} ${Headroom}`;
}
