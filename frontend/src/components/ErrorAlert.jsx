export default function ErrorAlert({ message }) {
  return (
    <div className="alert alert-danger mt-3" role="alert">
      {message}
    </div>
  );
}
