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

export const FEATURES = [
  {
    icon: "",
    title: "Upload any content",
    desc: "From PDFs and YouTube videos to slides and even recorded lectures, learn everything your way.",
  },
  {
    icon: "",
    title: "Test your knowledge",
    desc: "Create and customize flashcards: edit, delete, star, view sources, and more.",
  },
  {
    icon: "",
    title: "Sources Included",
    desc: "Retrieve accurate and contextual information from your content.",
  },
];

export const STEPS = [
  { img: "", title: "Create a workspace", desc: "" },
  { img: "", title: "Upload materials", desc: "Upload all your materials." },
  {
    img: "",
    title: "Get a cup of a coffee",
    desc: "Cause there's nothing better than a cup of coffee to get started with learning.",
  },
];

export const PRICES = [
  {
    title: "Free",
    price: "0",
    desc: "Start your learning journey here.",
    features: [
      "5 AI chats / day (includes 3/month with Learn+)",
      "3 PDFs or YouTube Links / month",
      "Upload PDFs, each up to 120 pages / 20 MB in size",
      "2 recorded lecture / month",
    ],
    button: "Get Started",
    isPrimary: false,
  },
  {
    title: "Pro (annual)",
    price: "1,000",
    desc: "Learn at the highest level.",
    features: [
      "Unlimited AI chats (includes 100/month with Learn+)",
      "Unlimited PDFs or YouTube Links",
      "Upload PDFs, each up to 2000 pages / 50 MB in size",
      "40 recorded lectures / month",
      "Access to advanced voice mode beta",
    ],
    button: "Choose Pro",
    isPrimary: true,
  },
];
