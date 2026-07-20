type PixelIconProps = {
  viewBox: string;
  children: React.ReactNode;
  className?: string;
  title: string;
};

const PixelIcon = ({ viewBox, children, className, title }: PixelIconProps) => {
  return (
    <svg className={`pixel-icon ${className ?? ""}`.trim()} viewBox={viewBox} aria-hidden="true" role="img" focusable="false" shapeRendering="crispEdges">
      <title>{title}</title>
      {children}
    </svg>
  );
};

export const HomePixelIcon = () => (
  <PixelIcon viewBox="0 0 16 16" title="Home">
    <rect x="3" y="7" width="10" height="7" className="pixel-icon-fill" />
    <rect x="2" y="7" width="12" height="2" className="pixel-icon-accent" />
    <rect x="5" y="9" width="2" height="5" className="pixel-icon-bg" />
    <rect x="9" y="9" width="2" height="5" className="pixel-icon-bg" />
    <rect x="5" y="3" width="6" height="4" className="pixel-icon-roof" />
    <rect x="7" y="1" width="2" height="2" className="pixel-icon-accent" />
  </PixelIcon>
);

export const CogPixelIcon = () => (
  <PixelIcon viewBox="0 0 16 16" title="Configuration">
    <rect x="6" y="1" width="4" height="2" className="pixel-icon-accent" />
    <rect x="6" y="13" width="4" height="2" className="pixel-icon-accent" />
    <rect x="1" y="6" width="2" height="4" className="pixel-icon-accent" />
    <rect x="13" y="6" width="2" height="4" className="pixel-icon-accent" />
    <rect x="4" y="4" width="8" height="8" className="pixel-icon-fill" />
    <rect x="5" y="5" width="6" height="6" className="pixel-icon-bg" />
    <rect x="7" y="7" width="2" height="2" className="pixel-icon-accent" />
  </PixelIcon>
);

export const StateStylesPixelIcon = () => (
  <PixelIcon viewBox="0 0 16 16" title="State Styles">
    <rect x="2" y="3" width="4" height="4" className="pixel-icon-accent" />
    <rect x="6" y="3" width="4" height="4" className="pixel-icon-fill" />
    <rect x="10" y="3" width="4" height="4" className="pixel-icon-roof" />
    <rect x="2" y="7" width="4" height="4" className="pixel-icon-fill" />
    <rect x="6" y="7" width="4" height="4" className="pixel-icon-roof" />
    <rect x="10" y="7" width="4" height="4" className="pixel-icon-accent" />
    <rect x="5" y="11" width="6" height="2" className="pixel-icon-bg" />
  </PixelIcon>
);

export const BoxPixelIcon = () => (
  <PixelIcon viewBox="0 0 16 16" title="Resource Pack">
    <rect x="3" y="4" width="10" height="8" className="pixel-icon-fill" />
    <rect x="4" y="5" width="8" height="1" className="pixel-icon-accent" />
    <rect x="4" y="7" width="8" height="1" className="pixel-icon-roof" />
    <rect x="7" y="4" width="2" height="8" className="pixel-icon-bg" />
    <rect x="2" y="3" width="12" height="1" className="pixel-icon-accent" />
    <rect x="2" y="12" width="12" height="1" className="pixel-icon-accent" />
  </PixelIcon>
);

export const InfoPixelIcon = () => (
  <PixelIcon viewBox="0 0 16 16" title="About">
    <rect x="7" y="7" width="2" height="6" className="pixel-icon-fill" />
    <rect x="7" y="4" width="2" height="2" className="pixel-icon-accent" />
    <rect x="5" y="7" width="2" height="2" className="pixel-icon-accent" />
    <rect x="9" y="7" width="2" height="2" className="pixel-icon-accent" />
    <rect x="6" y="13" width="4" height="1" className="pixel-icon-roof" />
  </PixelIcon>
);

export default PixelIcon;