import Notebook from "@/components/notebooks/Notebook";

type Props = {
  params: {
    id: string;
  };
};

export default function page(props: Props) {
  return <Notebook notebookId={props.params.id} />;
}
