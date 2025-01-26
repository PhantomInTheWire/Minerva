import { ScrollAnimatedContainer } from "@/components/ui";
import Text from "./Text";

export default function Introduction() {
  return (
    <div className="pb-40">
      <Text />
      <ScrollAnimatedContainer>
        <video autoPlay={true} loop muted className="roundex-3xl">
          <source src="./product-demo.mp4" type="video/mp4" />
        </video>
      </ScrollAnimatedContainer>
    </div>
  );
}
