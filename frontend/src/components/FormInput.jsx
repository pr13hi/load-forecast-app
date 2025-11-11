export function FormInput({ label, ...props }) {
  return (
    <div className="mb-3">
      <label className="form-label">{label}</label>
      <input className="form-control" {...props} />
    </div>
  );
}
