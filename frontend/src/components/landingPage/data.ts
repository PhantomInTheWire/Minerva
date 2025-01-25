type Action = {
  href: string;
  label: string;
  variant:
    | "link"
    | "outline"
    | "default"
    | "destructive"
    | "secondary"
    | "ghost"
    | null;
};
export const ACTIONS: Action[] = [
  {
    label: "See Features",
    href: "#features",
    variant: "outline",
  },
  {
    label: "Get Started",
    href: "#",
    variant: "default",
  },
];

export const PEOPLE = [
  {
    id: "135950363",
    name: "Karan",
    designation: "PhantomInTheWire",
  },
  {
    id: "47332922",
    name: "Ishu",
    designation: "ishu-codes",
  },
  {
    id: "146630018",
    name: "Priyanshu",
    designation: "R-Priyanshu",
  },
  {
    id: "153438162",
    name: "Yashvi",
    designation: "codebyyashvi",
  },
];

export const UNIVERSITIES = [
  "Michigan State University",
  "Massachusetts Institute of Technology",
  "University of Michigan",
  "Princeton University",
  "Stanford University",
  "Harvard University",
  "University of Pennsylvania",
  "University of California",
  "University of Chicago",
];
