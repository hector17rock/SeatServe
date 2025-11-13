import { useState } from 'react';

export default function Auth() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    setTimeout(() => {
      if (!email || !password) {
        setError('Please fill in all fields');
        setLoading(false);
        return;
      }

      // Allow any email/password combination - no validation
      localStorage.setItem('seatserve_user', email);
      localStorage.setItem('seatserve_logged_in', 'true');
      window.location.href = '/';

      setLoading(false);
    }, 500);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-cyan-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="flex justify-center mb-8">
          <div className="h-16 w-16">
            <img 
              src="/Images/seatserve-app-icon.png" 
              alt="SeatServe Logo" 
              className="w-full h-full object-contain" 
            />
          </div>
        </div>

        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-neutral-900 mb-2">SeatServe</h1>
          <p className="text-neutral-600">Order from your seat or pick up fast</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8 border border-neutral-200">
          <h2 className="text-xl font-semibold text-neutral-900 mb-6 text-center">
            Sign In or Create Account
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2">
                Email Address
              </label>
              <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter any email"
                className="w-full rounded-xl border border-neutral-300 px-4 py-3 text-neutral-900 placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter any password"
                className="w-full rounded-xl border border-neutral-300 px-4 py-3 text-neutral-900 placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent"
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="rounded-lg bg-red-50 border border-red-200 p-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-6 px-4 py-3 rounded-xl bg-gradient-to-r from-emerald-400 to-cyan-400 text-neutral-900 font-semibold hover:from-emerald-500 hover:to-cyan-500 focus:ring-2 focus:ring-emerald-400 focus:ring-offset-2 transition duration-200 disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Continue'}
            </button>
          </form>
        </div>

        {/* Demo Info */}
        <div className="mt-8 text-center text-xs text-neutral-500">
          <p>Use any email and password to enter</p>
        </div>
      </div>
    </div>
  );
}
