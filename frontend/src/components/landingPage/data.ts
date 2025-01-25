import { ISourceOptions, MoveDirection, OutMode } from "@tsparticles/engine";

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

export const PARTICLES_CONFIG: ISourceOptions = {
  background: {
    color: {
      value: "#0d47a1",
    },
  },
  fpsLimit: 120,
  interactivity: {
    events: {
      onClick: {
        enable: true,
        mode: "push",
      },
      onHover: {
        enable: true,
        mode: "repulse",
      },
    },
    modes: {
      push: {
        quantity: 4,
      },
      repulse: {
        distance: 200,
        duration: 0.4,
      },
    },
  },
  particles: {
    color: {
      value: "#ffffff",
    },
    links: {
      color: "#ffffff",
      distance: 150,
      enable: true,
      opacity: 0.5,
      width: 1,
    },
    move: {
      direction: MoveDirection.none,
      enable: true,
      outModes: {
        default: OutMode.out,
      },
      random: false,
      speed: 6,
      straight: false,
    },
    number: {
      density: {
        enable: true,
      },
      value: 80,
    },
    opacity: {
      value: 0.5,
    },
    shape: {
      type: "circle",
    },
    size: {
      value: { min: 1, max: 5 },
    },
  },
  detectRetina: true,
};
