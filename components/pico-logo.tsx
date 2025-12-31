export default function PicoLogo({ className = "w-8 h-8" }: { className?: string }) {
  return (
    <svg viewBox="0 0 80 80" className={className} fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <g transform="translate(-20, -17.142857142857142) scale(1.1428571428571428)" fill="currentColor">
        <g xmlns="http://www.w3.org/2000/svg">
          <path d="M27.5,85h60V25h-60V85z M32.5,55L45,35l15,25l12.5-12.5l10,12.5v20h-50V55z" />
          <polygon points="77.5,15 17.5,15 17.5,75 25,75 25,22.5 77.5,22.5  " />
        </g>
      </g>
    </svg>
  )
}
